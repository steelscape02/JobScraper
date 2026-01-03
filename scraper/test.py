import re

wage_test = "Contact NameGator ZauggCompanyGator ZauggContact Phone Number Live Pest ControlAddress(208) 851-4122Email Address 798 S Blvd Idaho Falls, IdahoJob Titlezaugg2025@gmail.comJob DescriptionThe Pest Control Installer / Service Technician is responsible for installing pest control systems, applying treatments, and providing customer support to ensure safe and effective pest prevention.This position includes paid training for the right candidate.· Install exclusion systems, traps, and pest prevention products· Perform routine pest control services at residential and commercial locations· Inspect properties to identify pest activity and entry points· Follow safety procedures, product labels, and service guidelines· Provide excellent customer service and answer basic client questions· Maintain service equipment, tools, and company vehicle· Complete service reports or digital logs after each jobRequirements / Qualifications· Valid driver’s license with a clean driving record· Ability to lift 40–50 lbs and work outdoors in varied conditions· Good communication and customer service skills· Willingness to learn, experience a plus but not required· Ability to work independently and manage time effectively.Benefits· Paid training and certifications· Advancement opportunities· Company vehicle during work hours (if applicable)Start Date· Monday–Saturday· Full-time, 40 hours/weekJob Type: Full-timePay: $18.00 - $24.00 per hourBenefits:· Fuel card· Opportunities for advancement· Paid trainingLicense/Certification: January 2026Duration/End DateN/AHours Monday-Saturday - 40 hours/weekPay/Wage $18.00-$24.00 per hourHow to Apply:How to Apply: Email your application to zaugg2025@gmail.com.Application Deadline: Application Deadline: March 2026Other Questions/Comments:thing"


def parse_wage(wage_str: str):
    x = re.search(r'Other Questions(/|\s/\s)Comments:(.*?)(?=$)', wage_str)
    print(x.group(2).strip() if x else None)

parse_wage(wage_test)

#Requirements(/|\s/\s)Qualifications(.*?)(?=Start Date)"