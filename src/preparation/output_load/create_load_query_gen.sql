
                    -- parameterized script generated with python
                    -- create table to load ownership data
                    drop table if exists opencmsdb.ownership;
                    create table if not exists opencmsdb.ownership (					
                    change_type text DEFAULT NULL, 
					physician_profile_id text DEFAULT NULL, 
					physician_first_name text DEFAULT NULL, 
					physician_middle_name text DEFAULT NULL, 
					physician_last_name text DEFAULT NULL, 
					physician_name_suffix text DEFAULT NULL, 
					recipient_primary_business_street_address_line1 text DEFAULT NULL, 
					recipient_primary_business_street_address_line2 text DEFAULT NULL, 
					recipient_city text DEFAULT NULL, 
					recipient_state text DEFAULT NULL, 
					recipient_zip_code text DEFAULT NULL, 
					recipient_country text DEFAULT NULL, 
					recipient_province text DEFAULT NULL, 
					recipient_postal_code text DEFAULT NULL, 
					physician_primary_type text DEFAULT NULL, 
					physician_specialty text DEFAULT NULL, 
					record_id text DEFAULT NULL, 
					program_year text DEFAULT NULL, 
					total_amount_invested_usdollars text DEFAULT NULL, 
					value_of_interest text DEFAULT NULL, 
					terms_of_interest text DEFAULT NULL, 
					submitting_applicable_manufacturer_or_applicable_gpo_name text DEFAULT NULL, 
					applicable_manufacturer_or_applicable_gpo_making_payment_id text DEFAULT NULL, 
					applicable_manufacturer_or_applicable_gpo_making_payment_name text DEFAULT NULL, 
					applicable_manufacturer_or_applicable_gpo_making_payment_state text DEFAULT NULL, 
					applicable_manufacturer_or_applicable_gpo_making_payment_count text DEFAULT NULL, 
					dispute_status_for_publication text DEFAULT NULL, 
					interest_held_by_physician_or_an_immediate_family_member text DEFAULT NULL, 
					payment_publication_date text DEFAULT NULL
                     					);
            


                    -- parameterized script generated with python
                    -- create table to load deleted data
                    drop table if exists opencmsdb.deleted;
                    create table if not exists opencmsdb.deleted (					
                    change_type text DEFAULT NULL, 
					program_year text DEFAULT NULL, 
					payment_type text DEFAULT NULL, 
					record_id text DEFAULT NULL
                     					);
            