from dotenv import load_dotenv
from openai import OpenAI
import base64
import os
from pathlib import Path
import json

client = OpenAI()
load_dotenv()

def call_openai_for_entity_division(input_section_str: str):

  system_prompt = """You are an experienced seasoned underwriter working in Senior Living Insurance Facility space. 
  You know all the important information that you need from an application to write the best coverage policy.

  You will be provided with OCRed text of the application. Classify the information into the right entity. 
  
  Entities: 1. Facility, 2. Residents, 3. Claims history, 4. Licensing and Ceritfication,
  5. Risk Management, 6. Contracted Services, 7. Physical Premises and Security, 8. Corporate Structure, 
  9. Bed Census and Occupancy, 10. Coverage, 11. Services, 12. Incidents, 13. Staffing.
  """

  example_prompt_1 = """
  Facility Information

  Facility Name: Senior Living LLC
  Facility Address: 1234 Northside Blvd
  City: Richardson    State: TX    Zip: 75080
  Federal Employer ID #: 12-3424221
  Administrator Name: Ricky Bahal    Telephone: 838-332-2839
  Email Address: ricky@seniorliving.com    Fax: (___)___-____

  How many years has the facility been under: Present ownership? 5   Present management? 3

  Has the facility had its license suspended, revoked, placed on probation in the last 5 years? ☐ Yes ☑ No
    If yes, please explain: ________________________

  Has Medicare or Medicaid certification been suspended or revoked in the last 3 years? ☐ Yes ☑ No
    If yes, please explain: ________________________

  Has a state or federal agency fined this facility in the last 3 years? ☐ Yes ☑ No

  Has the applicant been designated as a Special Focus Facility within the past 2 years? ☐ Yes ☑ No
  """

  assistant_prompt_1 = """
    1. Facility
    Facility Name: Senior Living LLC
    Facility Address: 1234 Northside Blvd
    City: Richardson
    State: TX
    Zip: 75080
    Federal Employer ID #: 12-3424221
    Years under present ownership: 5
    Years under present management: 3

    13. Staffing
    Administrator Name: Ricky Bahal
    Telephone: 838-332-2839
    Email Address: ricky@seniorliving.com
    Fax: Not provided

    4. Licensing and Certification
    License suspension, revocation, or probation in the last 5 years: No
    Medicare or Medicaid certification suspension or revocation in the last 3 years: No
    Fines by state or federal agency in the last 3 years: No
    Designation as a Special Focus Facility within the past 2 years: No
    """

  example_prompt_2 = """
  Director of Nursing (DON): Name: Julian Caeser ☐ RN ☐ LPN  
  Length of time at this facility: 12   Length of time as DON: 5  
  Total Number of Director of Nursing at the Facility in the last 5 years: 1  
  Total # of nurse employees: 23  

  Category            | 1st shift | 2nd shift | 3rd shift | Turnover %  
  --------------------|-----------|-----------|-----------|------------  
  RN                 |      3    |      2    |           |   100%  
  LPN/LVN            |      2    |      3    |           |    80%  
  CNA/Personal Caregiver | 1    |      4    |           |    80%  
  Agency / Pool      |      4    |      3    |     1     |   87.5%  

  Do you require nurses to carry malpractice coverage? ☐ Yes ☑ No  
  Do you verify nursing licenses & CRNA certification upon hire and annually? ☑ Yes ☐ No  
  Are background checks completed for agency and pool employees? ☑ Yes ☐ No  
  Are any employees members of a labor union? ☐ Yes ☑ No  

  Are Criminal Background Checks and Sexual Offender Registry Searches performed regularly on ALL staff and volunteers? ☑ Yes ☐ No  
    If “No”, please explain: ______________________  

  Total number of volunteers? 4  
  Is there a formal screening & orientation process? ☑ Yes ☐ No  

  Do volunteers assist with resident feeding? ☑ Yes ☐ No  
  """
  assistant_prompt_2 = """
    13. Staffing
    Director of Nursing (DON)
    Name: Julian Caeser
    Certification: Not specified (neither RN nor LPN box checked)
    Length of time at this facility: 12 years
    Length of time as DON: 5 years
    Total Number of DONs at the Facility in the last 5 years: 1
    Nurse Employees
    Total number of nurse employees: 23
    Staffing Distribution
    Category            | 1st shift | 2nd shift | 3rd shift | Turnover %  
    --------------------|-----------|-----------|-----------|------------  
    RN                 |      3    |      2    |           |   100%  
    LPN/LVN            |      2    |      3    |           |    80%  
    CNA/Personal Caregiver | 1    |      4    |           |    80%  
    Agency / Pool      |      4    |      3    |     1     |   87.5%  
    Staff Policies and Procedures
    Requirement for nurses to carry malpractice coverage: No
    Verification of nursing licenses & CRNA certification upon hire and annually: Yes
    Background checks for agency and pool employees: Yes
    Employees as members of a labor union: No
    Criminal Background Checks and Sexual Offender Registry Searches on ALL staff and volunteers: Yes
    Volunteers
    Total number of volunteers: 4
    Formal screening & orientation process for volunteers: Yes
    Volunteers assist with resident feeding: Yes

    5. Risk Management
    Verification of nursing licenses & CRNA certification upon hire and annually
    Background checks for agency and pool employees
    Criminal Background Checks and Sexual Offender Registry Searches on ALL staff and volunteers
    Formal screening & orientation process for volunteers
    """

  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user","content": [{ "type": "text", "text": example_prompt_1}]},
    {"role": "assistant","content": [{ "type": "text", "text": assistant_prompt_1}]},
    {"role": "user","content": [{ "type": "text", "text": example_prompt_2}]},
    {"role": "assistant","content": [{ "type": "text", "text": assistant_prompt_2 }]},
    {"role": "user","content": [{ "type": "text", "text": input_section_str}]},
  ]


  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature = 0.01
  )
  
  return completion.choices[0].message.content

  


  

  