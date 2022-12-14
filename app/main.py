from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.sql import select,text


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


    final_query = session.query(q).outerjoin(
         q1,q1.columns.ai_resource_idai_resource == q.columns.title_1
    ).outerjoin(
        q2,q2.columns.ai_resource_idai_resource == q.columns.title_1
    ).outerjoin(
        q3,q3.columns.ai_resource_idai_resource == q.columns.title_1
    ).outerjoin(
        q4,q4.columns.ai_resource_idai_resource == q.columns.title_1).all()

    return {"message": "OK"}