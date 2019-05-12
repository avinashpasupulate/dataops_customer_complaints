drop table if exists custcomp_db.customer_complaints
create table if not exists custcomp_db.customer_complaints (
        date_received text,
        product text,
        sub_product text,
        issue text,
        sub_issue text,
        consumer_complaint_narrative text,
        company_public_response text,
        company text,
        company_state text,
        zip_code text,
        tags text,
        consumer_consent_provided text,
        submitted_via text,
        date_sent_to_company text,
        company_response_to_consumer text,
        timely_response text,
        consumer_disputed text,
        complaint_id text
);

load data local infile '/Users/Avinash/Documents/datascience/dataops/data/raw/Consumer_Complaints.csv'
into table custcomp_db.customer_complaints fields terminated by ',' enclosed by '"' ignore 1 rows;


select * from customer_complaints limit 10;