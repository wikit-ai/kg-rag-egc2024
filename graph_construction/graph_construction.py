import os
import pandas as pd

from py2neo import Graph

## ----- INITIALISATION -----
uri = os.environ.get("GRAPH_URI")
user = os.environ.get("GRAPH_USER")
password = os.environ.get("GRAPH_PASSWORD")
transformations_dataset = "transformations.xlsx"

graph = Graph(uri=uri, user=user, password=password)

## ----- CONSTRAINTS DEFINITION -----
graph.run("CREATE CONSTRAINT ON (g:Goal) ASSERT g.code IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (t:Target) ASSERT t.code IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (i:Indicator) ASSERT i.code IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (c:Transformation) ASSERT c.code IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (c:IntermediateOutput) ASSERT c.title IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (c:Intervention) ASSERT c.title IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (c:Ministry) ASSERT c.title IS UNIQUE;")

## ----- COLLECT AND IMPORT GOALS -----
graph.run(
    """CALL apoc.load.json("https://unstats.un.org/SDGAPI/v1/sdg/Goal/List?includechildren=false")
    YIELD value
    UNWIND value AS goal
    MERGE (g:Goal {code: toString(goal.code)})
    SET g.title = toString(goal.title)
    SET g.description = toString(goal.description);"""
)

## ----- COLLECT AND IMPORT TARGETS PER GOAL -----
graph.run(
    """MATCH (g:Goal)
    CALL apoc.load.json("https://unstats.un.org/SDGAPI/v1/sdg/Goal/"+g.code+"/Target/List?includechildren=true")
    YIELD value
    UNWIND value.targets AS target
    MERGE (t:Target {code: toString(target.code)})
    SET t.title = toString(target.title)
    SET t.description = toString(target.description)
    MERGE (t)<-[r2:HAS_TARGET]-(g);"""
)

## ----- COLLECT AND IMPORT INDICATOR PER TARGET -----
graph.run(
    """MATCH (t:Target)
    CALL apoc.load.json("https://unstats.un.org/SDGAPI/v1/sdg/Target/"+t.code+"/Indicator/List?includechildren=true")
    YIELD value
    UNWIND value.indicators AS indicator
    MERGE (i:Indicator {code: toString(indicator.code)})
    SET i.title = toString(indicator.title)
    SET i.description = toString(indicator.description)
    MERGE (s:Source{name:'UN_SDG'})
    MERGE (t)-[r1:HAS_INDICATOR]->(i)-[r2:COMES_FROM]->(s);"""
)

## ----- COLLECT AND IMPORT TRANSFORMATIONS -----
tx = graph.auto()
df_6t = pd.read_excel(transformations_dataset, engine="openpyxl", sheet_name="Info")
params = []
statement = """
    UNWIND $parameters as row
    MERGE (t:Transformation{title:row.title,code:row.code})
    """

for index, row in df_6t.iterrows():
    params_dict = {"title": str(row["Title"]), "code": int(row["Transformation"])}
    params.append(params_dict)

tx.evaluate(statement, parameters={"parameters": params})

## ----- COLLECT AND IMPORT INTERVENTION AND INTERMEDIATE OUTPUTS -----
tx = graph.auto()
df_int = pd.read_excel(transformations_dataset, sheet_name="IntOutput")
params = []
statement = """
    UNWIND $parameters as row
    MATCH (t:Transformation{code:row.code})
    MERGE (i:Intervention{title:row.int_title})
    MERGE (int:IntermediateOutput{title:row.io_title})
    MERGE (t)-[:COMPRISES]->(i)
    MERGE (i)-[:CONTRIBUTES_TO]->(int)
    """

for index, row in df_int.iterrows():
    params_dict = {
        "code": int(row["Transformation"]),
        "int_title": str(row["Interventions"]),
        "io_title": str(row["IntermediateOutput"]),
    }
    params.append(params_dict)

tx.evaluate(statement, parameters={"parameters": params})

## ----- ASSOCIATION BETWEEN SDGs AND INTERMEDIATE OUTPUTS -----
tx = graph.auto()
transf_dict = {
    "1": "enables the SDG",
    "2": "reinforces the SDG",
    "3": "directly targets the SDG",
}

df_int_sdg = pd.read_excel(transformations_dataset, sheet_name="SDG_Weights")
df = df_int_sdg.loc[df_int_sdg["Weight"] != 0]
params = []
statement = """
    UNWIND $parameters as row
    MATCH (g:Goal{code:row.code})
    MATCH (int:IntermediateOutput{title:row.io_title})
    MERGE (int)-[:ASSOCIATED_WITH{weight:row.weight,description:row.desc}]->(g)
    """

for index, row in df.iterrows():
    params_dict = {
        "code": str(row["SDG"]),
        "weight": int(row["Weight"]),
        "desc": transf_dict[str(row["Weight"])],
        "io_title": str(row["Outputs"]),
    }
    params.append(params_dict)

tx.evaluate(statement, parameters={"parameters": params})

## ----- ASSOCIATION BETWEEN TRANSFORMATIONS AND MINISTRIES -----
tx = graph.auto()
df_min = pd.read_excel(transformations_dataset, sheet_name="Ministry")
params = []
statement = """
    UNWIND $parameters as row
    MATCH (t:Transformation{code:row.code})
    MERGE (m:Ministry{title:row.m_title})
    MERGE (m)-[:OVERSEE_THE_IMPLEMENTATION_OF]->(t)
    """

for index, row in df_min.iterrows():
    params_dict = {"code": int(row["Transformation"]), "m_title": str(row["Ministry"])}
    params.append(params_dict)

tx.evaluate(statement, parameters={"parameters": params})
