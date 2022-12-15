from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.sql import select,text
import json
from fastapi.encoders import jsonable_encoder



app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:mypassword@172.17.0.3:3306/mydb"
engine = sa.create_engine(DATABASE_URL)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


inspector = inspect(engine)
tables = inspector.get_table_names()


@app.get("/")
def read_root():
    ai_resource = sa.Table('ai_resource', sa.MetaData(), autoload_with=engine)
    resource_type = sa.Table('resource_type', sa.MetaData(), autoload_with=engine)
    ai_resource_has_application_area = sa.Table('ai_resource_has_application_area',sa.MetaData(), autoload_with=engine)
    application_area = sa.Table('application_area', sa.MetaData(), autoload_with=engine)
    ai_resource_has_research_area = sa.Table('ai_resource_has_research_area',sa.MetaData(), autoload_with=engine)
    research_area = sa.Table('research_area', sa.MetaData(), autoload_with=engine)
    person = sa.Table('person', sa.MetaData(), autoload_with=engine)
    ai_resource_has_contact_person = sa.Table('ai_resource_has_contact_person', sa.MetaData(), autoload_with=engine)
    organisation = sa.Table('organisation', sa.MetaData(), autoload_with=engine)
    ai_resource_developed_by_organisation = sa.Table('ai_resource_developed_by_organisation', sa.MetaData(), autoload_with=engine)

    q = session.query(
    ai_resource.columns.title ,
    ai_resource.columns.description,
    resource_type.columns.title,
    ).outerjoin( 
        resource_type,resource_type.columns.idresource_type == ai_resource.columns.resource_type_id
    ).subquery()



    q1 = session.query(
        ai_resource_has_research_area.columns.ai_resource_idai_resource,
        research_area.columns.title
    ).filter(
        research_area.columns.idresearch_area == ai_resource_has_research_area.columns.research_area_idresearch_area
    ).subquery()

    q2 = session.query(
        ai_resource_has_application_area.columns.ai_resource_idai_resource,
        application_area.columns.title
    ).filter(
        application_area.columns.idapplication_area == ai_resource_has_application_area.columns.application_area_idapplication_area
    ).subquery()

    q3 = session.query(
        ai_resource_has_contact_person.columns.ai_resource_idai_resource,
        person.columns.full_name,
        person.columns.email
    ).filter(
        ai_resource_has_contact_person.columns.person_idperson == person.columns.idperson
    ).subquery()


    q4 = session.query(
        ai_resource_developed_by_organisation.columns.ai_resource_idai_resource,
        organisation.columns.title,
        organisation.columns.description,
        organisation.columns.website

    ).filter(
        ai_resource_developed_by_organisation.columns.organisation_idorganisation == organisation.columns.idorganisation
    ).subquery()



    final_query = session.query(
                        ai_resource.c.title,
                        ai_resource.c.description,
                        q1.c.title,
                        q2.c.title,
                        q3.c.full_name,
                        q3.c.email,
                        q4.c.title,
                        q4.c.description,
                        q4.c.website
    
                    ).join(
                        resource_type,resource_type.columns.idresource_type == ai_resource.columns.resource_type_id
                    ).outerjoin(
                        q1,q1.columns.ai_resource_idai_resource == ai_resource.columns.idai_resource
                    ).outerjoin(
                        q2,q2.columns.ai_resource_idai_resource == ai_resource.columns.idai_resource
                    ).outerjoin(
                        q3,q3.columns.ai_resource_idai_resource == ai_resource.columns.idai_resource
                    ).outerjoin(
                        q4,q4.columns.ai_resource_idai_resource == ai_resource.columns.idai_resource)
    
    query_results = final_query.all()
    results = [] 
    
    for result in query_results:
        results_as_dict = {}
        results_as_dict["resource_title"] = result[0]
        results_as_dict["resource_description"] = result[1]
        results_as_dict["resource_research_area"] = result[2]
        results_as_dict["resource_application_area"] = result[3]
        results_as_dict["contact_person_full_name"] = result[4]
        results_as_dict["contact_person_email"] = result[5]
        results_as_dict["organisation_title"] = result[6]
        results_as_dict["organisation_description"] = result[7]
        results_as_dict["organisation_website"] = result[8]
        
        
        results.append(results_as_dict)
    json_results = jsonable_encoder(results)
    # json_results = json.dumps(results, indent=2)
    
    return json_results