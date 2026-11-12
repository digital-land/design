---
prefix: govuk
reference: guidance/publish-your-developer-contributions-data
name: Publish your developer contributions data
entry-date: 2026-11-11T17:17:34Z
start-date: 2019-09-01
document-url: https://www.gov.uk/guidance/publish-your-developer-contributions-data
---

# Publish your developer contributions data

## Publish your data

The Community Infrastructure Levy (CIL) regulations require all local planning authorities that issue a CIL liability notice or enter into section 106 planning obligations during a reporting year to publish an infrastructure funding statement (IFS) at least annually. The infrastructure funding statement should, as a minimum, include the information set out in [Schedule 2 to the Community Infrastructure Levy regulations 2010](https://www.legislation.gov.uk/ukdsi/2010/9780111492390/contents) (as inserted by the 2019 regulations).

In addition, it is recommended that local authorities also publish the raw data that informed the infrastructure funding statement. This guidance sets out a data format and approach that you can follow in order to publish data that sits behind the infrastructure statement.

The data format and infrastructure funding statements will give policy makers and communities better insight into how developer contributions are supporting new development and local infrastructure. We have designed the data format to cause as little disruption as possible to existing processes.

Please share your feedback on this guidance by filling out a [feedback form](https://docs.google.com/forms/d/e/1FAIpQLSemGYaMzQrMpO_e2v3zl_IbOyMX0UpnuK_CZTDnKuCfLIm9wA/viewform) or by emailing [DigitalLand@communities.gov.uk](mailto:DigitalLand@communities.gov.uk).

### Make your data findable, useable and trustworthy

Developer contributions include section 106 planning obligations, CIL, section 278 agreements and any agreements that either secure funding towards new development, or provide infrastructure as part of any new development. This data has a wide range of current and potential uses, including:

- planning land and housing development
- creating new digital services
- giving community members insight into local development and how they can influence it

But for data to be useful it must be easy to find, use, understand and trust. It is recommended that local planning authorities ensure that their developer contributions data is all of these by following this specification for how to format, label and publish it. The following guidance gives a high-level overview of the data format and the publication process.

Local authorities should continue to publish section 106 agreements on the planning register. Publishing your developer contributions data in this format will help you fill out your infrastructure funding statement but does not replace that requirement.

The Digital Land team at the Ministry of Housing, Communities & Local Government (MHCLG) are working to support the process of producing an infrastructure funding statement, using the data published in accordance with this guidance. They will update the [Digital Land website](https://digital-land.github.io/project/infrastructure-funding-statement/) with progress on this.

The Digital Land team at the Ministry of Housing, Communities & Local Government (MHCLG) are developing tools to collect and present the data. They will update the [Digital Land website](https://digital-land.github.io/project/infrastructure-funding-statement/) with progress on this.

### Publishing developer contributions: 3 steps

Planning authorities must publish their infrastructure funding statements once a year, but may publish the underlying data more frequently so that datasets are up to date. (Those publishing with third-party software that can semi-automate the process might be able to publish in near real-time, while those publishing manually might choose to only publish quarterly.)

This guidance applies to the publication of developer contributions data going forward – you are not required to republish historical data, other than for CIL revenues and planning obligations previously received which remain unspent.

Publishing is a 3 step process:

1. Create 3 developer contribution CSV files to store the data
2. Upload each of these files to your organisation’s website and give them a persistent URL, then clearly link to them from your developer contributions web page
3. Submit the URLs you created in Step 2 to the national register of developer contributions

## Step 1: Create your CSV files

To complete step 1 you must be able to create or amend CSV files, for example by using spreadsheet software such as Microsoft Excel, Google Sheets or Apple Numbers.

If you are a planning authority using third-party software to manage your developer contributions, ask your vendor if the software can export the data to CSV files as defined in this guidance. If they are able to automatically generate the required .csv files, follow step 2 in order to publish the files. Otherwise, use the following instructions.

Developer contributions data must be entered in 3 separate CSV files. A CSV file (or comma separated value file) is a universally recognised file format for storing tabular data in plain text. Storing the data in 3 separate files rather than 1 file reduces duplication and makes the data easier to use and maintain.

We’ve created a CSV template for each of the 3 files:

- [developer agreements](https://digital-land.github.io/guidance/developer-contributions/developer-agreement_YYYYMMDD.csv)
- [developer agreement contributions](https://digital-land.github.io/guidance/developer-contributions/developer-agreement-contribution_YYYYMMDD.csv)
- [developer agreement transactions](https://digital-land.github.io/guidance/developer-contributions/developer-agreement-transaction_YYYYMMDD.csv)

If it helps, you can use the above example files and enter your developer contributions data. You must follow the guidelines below, then ‘save as .csv file’. To avoid the need to reformat the files each time you open them, you can save then, for example, as an Excel file and convert to a .csv file when you are ready to upload them for publication.

Each of the CSV files must:

- be named using the convention specified in each section below
- contain certain column headers (written exactly as shown, in lowercase)
- include 1 row of data for each agreement, contribution or transaction (as relevant)
- only contain entries that conform to the constraints described below

[Find out more about creating a CSV file](http://w3c.github.io/csvw/primer/).

The data model has been designed to accommodate the differences between recording planning obligations and CIL.

If you don’t have information for any fields, you can leave them blank.

## Developer agreements

A developer agreement is any legal document that secures contributions from a development for infrastructure or affordable housing (including section 106 planning obligations and section 278 agreements), or any demand notice for CIL.

[Do not delete or overwrite old or superseded agreements](https://digital-land.github.io/guidance/data-principles/#not-deleting-entries-in-a-register), but simply fill in the ‘end-date’ field.

### Name your CSV file

Developer agreements must be listed in a CSV file named exactly as follows, but with the actual date you created the file instead of YYYYMMDD:

developer-agreement_YYYYMMDD.csv

### Column headers:

#### developer-agreement

Create a unique identifier for the agreement. By ‘unique’ this means it should not be used for anything else in your organisation. (You could, for example, use the relevant planning application number appended with a suffix such as ‘-da’.)

#### organisation

[Find your organisation in this list](https://www.planning.data.gov.uk/organisation/) (in most cases this will be a local planning authority). Text must follow the same letter casing, with no spaces. Norfolk’s local planning authority, for example, would be:

local-authority-eng:NFK

Read the MHCLG Digital Land team’s [data principles](https://digital-land.github.io/guidance/data-principles/) for more information on dates.

#### entry-date

Enter the date that you record this data (for example today’s date), in the format YYYY-MM-DD. For 1 February 2019, for example, you should enter 2019-02-01.

#### start-date

For section 106 planning obligations, enter the date the agreement was ‘signed and sealed’. For CIL, enter the date the demand notice was issued.

If the original section 106 agreement or CIL demand notice is superseded by a new version (for example a deed of variation), enter the date on which the new version was agreed. This would be entered as a new entry, on a new line, rather than overwriting the original date. The ‘unique identifier’ would remain the same.

Enter the date in the same format as the entry-date column.

#### end-date

Leave this blank if this version of the section 106 agreement or CIL demand notice has not been superseded by a new one. If it has, enter the last day this version was in effect, in the same format as the entry-date column.

#### planning-application

Enter the unique, public facing reference number for the planning application.

#### document-url

Enter the web address that links directly to the actual agreement document or CIL demand notice. If your CIL demand notices are not published, leave this blank.

#### developer-agreement-type

This is either ‘community-infrastructure-levy’, ‘section-106’ or ‘section-278’. More developer agreement types will gradually be added to the [developer-agreement-type.csv](https://github.com/digital-land/alpha-data/blob/master/mhclg-registers/developer-agreement-type.csv) file, which MHCLG will maintain for your reference.

## Developer agreement contributions

Developer agreement contributions are the individual obligations or sums within an agreement, assigned to particular purposes such as affordable housing.

If CIL is being paid by instalments, each instalment should be recorded separately.

For CIL, the total sum should be split into the 3 separate developer agreement contribution purposes (administration, mayoral and neighbourhood). This is the case even if the CIL is being paid by instalments, and each instalment should also be recorded separately.

### Name your CSV file

Developer agreement contributions must be listed exactly as follows, but with the actual date you created the file instead of YYYYMMDD:

developer-agreement-contribution_YYYYMMDD.csv

### Column headers:

#### developer-agreement-contribution

Create a unique identifier for the contribution.

#### developer-agreement

Enter the unique identifier you’ve created for the agreement.

#### contribution-purpose

Enter the ID for the primary purpose of the developer contribution, as listed on our [developer contribution purpose page](https://www.planning.data.gov.uk/entity/?dataset=contribution-purpose) (for example the ID for transport and travel is transport-and-travel).

For CIL, if you have split the payment between neighbourhood CIL and administrative costs you can use the relevant ID from the above link. If you cannot split the payment you can enter one line for the total CIL amount.

#### amount

Enter the agreed, secured contribution amount, in pounds and pence but without a currency symbol or commas (for example 100000.00).

#### units

If the developer has agreed a non-financial contribution you should quantify that here (for example enter 100 if that many affordable housing units have been promised, or enter 2 for 2 public playgrounds). This field is not applicable for CIL.

Read the MHCLG Digital Land team’s [data principles](https://digital-land.github.io/guidance/data-principles/) for more information on dates.

#### entry-date

Enter the date that you record this data (for example today’s date), in the format YYYY-MM-DD. For 1 February 2019, for example, you should enter 2019-02-01.

#### start-date

For section 106 planning obligations, enter the date the agreement was ‘signed and sealed’. For CIL, enter the date the demand notice was issued.

If the original section 106 agreement or CIL demand notice is superseded by a new version (for example a deed of variation), enter the date on which the new version was agreed.

Enter the date in the same format as the entry-date column.

#### end-date

Leave this blank if this version of the section 106 agreement or CIL demand notice has not been superseded by a new one. If it has, enter the last day this version was in effect, in the same format as the entry-date column.

## Developer agreement transactions

### Name your CSV file

Developer agreement transactions must be listed in a CSV file exactly as follows, but with the actual date you created the file instead of YYYYMMDD:

developer-agreement-transaction_YYYYMMDD.csv

### Column headers:

#### developer-agreement-transaction

Create a unique identifier for the transaction.

#### developer-agreement-contribution

Enter the unique identifier you created for the contribution. For CIL spent money you will not be able to enter a contribution ID, so in this instance it can be left blank.

#### contribution-funding-status

Enter one of the below status IDs to indicate which stage the contribution is currently in.

If more than one status applies (for example if some money was spent and some returned), please create a separate row for each status.

If you have questions about what you should include or which stage your contribution is in, please email [CIL@communities.gov.uk](mailto:CIL@communities.gov.uk).

CIL:

- ‘secured’: the demand notice has been issued and the developer is now required to pay all or part of their CIL liability
- ‘received’: the developer has paid all or part of the money due to the local planning authority

You only need to record CIL up to the point of ‘received’, because money spent on CIL cannot be linked to an individual agreement. You can give details about CIL spending in your infrastructure funding statement.

Section 106 or 278:

- ‘secured’: the trigger clauses associated with the contribution have been met, meaning the developer is now required to pay all or part of the contribution
- ‘received’: the developer has paid all or part of the money due to the local planning authority
- ‘allocated’: the received money has been allocated to a team within the local planning authority, who will spend the money
- ‘transferred’: the received money has been transferred to an organisation outside the planning authority (for example another local authority or Transport for London), who will spend the money
- ‘spent’: the received money has been spent on the purpose specified in the section 106 or 278 agreement
- ‘returned’: the received money (or a portion of it) has been returned to the developer

#### amount

Enter the amount of money for each funding status.

Enter the amount as a numeric value for example £10,000 would be entered as 10000.00

#### units

If the developer has agreed a non-financial contribution you should quantify how much of that commitment has been met for this transaction if you can (for example enter 50 if 100 affordable housing units were committed and 50 have been delivered). This field will not be applicable for CIL so it can be left blank.

Read the MHCLG Digital Land team’s [data principles](https://digital-land.github.io/guidance/data-principles/) for more information on dates.

#### entry-date

Enter the date that you record this data (for example today’s date), in the format YYYY-MM-DD. For 1 February 2019, for example, you should enter 2019-02-01.

#### start-date

Enter the date on which this contribution status came into effect (for example the date that money was transferred or allocated), in the same format as the entry-date column.

#### end-date

Leave this blank if this version of the section 106 agreement or CIL demand notice has not been superseded by a new one. If it has, enter the last day this version was in effect, in the same format as the entry-date column.

## Step 2: Update your developer contributions web page

To complete step 2 you must be able to upload the files created in step 1 to your local planning authority’s website and edit (or create) your developer contributions web page. If you are not able or authorised to do this, speak to someone who is (this might be the person who updates your local planning authority’s brownfield site register or planning application web pages).

Upload each CSV file to your local planning authority’s website. Make sure the URL for each CSV file is [persistent](https://en.wikipedia.org/wiki/Persistent_uniform_resource_locator) (a web address that will not change over time). As an example, Norfolk’s local planning authority might use the following persistent addresses (note that these are examples, not live data):

https://www.norfolk.gov.uk/developer-agreement

https://www.norfolk.gov.uk/developer-agreement-contribution

https://www.norfolk.gov.uk/developer-agreement-transaction

When you upload the files you should keep any older files online – it’s important to retain a history of all developer contribution files.

You should then update your local planning authority’s developer contributions web page to make the CSV files publicly available. If your website does not have a page on developer contributions, you or someone in the web team will need to create one. We recommend publishing your developer contributions on the same web page as your authority’s infrastructure funding statement.

The page must list the persistent URLs as defined above. The URLs must be written out in full. (The URLs should not change. However, if they do, you must tell us.)

### Licensing

You must state on your web page that the data is provided under the [Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Step 3: Submit the URLs you created in Step 2 to the national register of developer contributions

MHCLG will maintain a national register of developer contributions.

Email the persistent URL for each CSV file to [DigitalLand@communities.gov.uk](mailto:DigitalLand@communities.gov.uk) and we will add them to the national register. You must tell us if these URLs ever change.

If have any questions or feedback, fill in this [feedback form](https://forms.microsoft.com/pages/responsepage.aspx?id=EGg0v32c3kOociSi7zmVqEQgqYxqOTBNlBUIVnxn62BUMTY5SDNIRTUxWkNNTDBGQ0dJN0hPTkZZVi4u&origin=lprLink&route=shorturl) or email [DigitalLand@communities.gov.uk](mailto:DigitalLand@communities.gov.uk)
