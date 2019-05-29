
                    -- parameterized script generated with python
                    -- create table to load b_ownership data
                    drop table if exists opencmsdb.b_ownership;
                    create table if not exists opencmsdb.b_ownership (					
                    change_type text, 
					physician_profile_id text, 
					physician_first_name text, 
					physician_middle_name text, 
					physician_last_name text, 
					physician_name_suffix text, 
					recipient_primary_business_street_address_line1 text, 
					recipient_primary_business_street_address_line2 text, 
					recipient_city text, 
					recipient_state text, 
					recipient_zip_code text, 
					recipient_country text, 
					recipient_province text, 
					recipient_postal_code text, 
					physician_primary_type text, 
					physician_specialty text, 
					record_id text, 
					program_year text, 
					total_amount_invested_usdollars text, 
					value_of_interest text, 
					terms_of_interest text, 
					submitting_applicable_manufacturer_or_applicable_gpo_name text, 
					applicable_manufacturer_or_applicable_gpo_making_payment_id text, 
					applicable_manufacturer_or_applicable_gpo_making_payment_name text, 
					applicable_manufacturer_or_applicable_gpo_making_payment_state text, 
					applicable_manufacturer_or_applicable_gpo_making_payment_count text, 
					dispute_status_for_publication text, 
					interest_held_by_physician_or_an_immediate_family_member text, 
					payment_publication_date text
                     					);
            