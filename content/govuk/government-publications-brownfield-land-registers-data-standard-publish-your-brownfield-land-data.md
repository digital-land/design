---
prefix: govuk
reference: government/publications/brownfield-land-registers-data-standard/publish-your-brownfield-land-data
name: Publish your brownfield land data
entry-date: 2026-11-11T19:22:07Z
start-date: 2019-10-31
document-url: https://www.gov.uk/government/publications/brownfield-land-registers-data-standard/publish-your-brownfield-land-data
documentation-url: https://www.gov.uk/government/publications/brownfield-land-registers-data-standard
---

# Publish your brownfield land data

## Publish your brownfield land data

[The Town and Country Planning (Brownfield Land Register) Regulations 2017](http://www.legislation.gov.uk/uksi/2017/403/contents/made) require local planning authorities to maintain a register of their brownfield sites that are suitable for housing. This guidance will help local planning authorities ensure brownfield land registers are:

- published in the agreed format and contain the required data
- kept up to date
- easily found online

Share any feedback on this guidance by emailing [DigitalLand@communities.gov.uk](mailto:DigitalLand@communities.gov.uk)

### Make your data findable, usable and trustworthy

Brownfield land is an important part of sustainable local planning and development. Data on brownfield land has a wide range of uses, including:

- planning for housing-led development
- creating new digital services
- giving community members insight into local development

But for data to be useful it must be easy to find, use, understand and trust. Local planning authorities should ensure that their brownfield land data is all of these by following this guidance on the data format and the publication process.

As a local planning authority, you must review your brownfield land register at least once a year. However, you should update your register as soon as a new brownfield site is identified or an existing one changes status, to increase trust in the data.

In the future, add any new brownfield sites as a new row to your published CSV file. If a site is no longer considered brownfield land, do not delete this entry but simply fill in the “EndDate” field.

### Publishing is a 3 step process:

1. Create a brownfield land CSV file
2. Upload the file to your organisation’s website and give it a persistent URL, then clearly link to this from your brownfield land web page
3. Update the national brownfield land register on the Ministry of Housing, Communities and Local Government website

You may not be able or authorised to complete all steps. Each step identifies the skills and authority required to complete it.

## Step 1: Create your CSV file

To complete step 1 you must be able to create or amend CSV files using spreadsheet software such as Microsoft Excel, Google Sheets or Apple Numbers, then when saving simply select ‘save as .csv file’. Find out more about [creating a CSV file](http://w3c.github.io/csvw/primer/).

Name your CSV file “brownfield-land.csv”.

We’ve created a [brownfield land data CSV template](https://digital-land.github.io/guidance/brownfield-sites/brownfield-sites.csv). If it helps, you can use this example file and enter your own data, following the guidelines below.

The [previous specification for brownfield land data](https://www.gov.uk/government/publications/brownfield-land-registers-data-standard) contained several column headers that aren’t listed here. Those fields are now optional. The ‘MinNetDwellings’ field has been replaced by ‘NetDwellingsRangeFrom’ and ‘NetDwellingsRangeTo’.

The following columns no longer exist, but any content that you already have in these fields can be added to the ‘Notes’ column:

- DevelopmentDescription
- SiteInformation
- NonHousingDevelopment
- ProposedForPIP

### Field definitions and formatting

The CSV file must include:

- a header row which must be the first row in the spreadsheet, written exactly as below (headers are case sensitive with no spacing)
- 1 row for each brownfield site

#### OrganisationURI

[Find your organisation in this list](https://www.planning.data.gov.uk/organisation/) and enter the corresponding Open Data Communities URI.

#### SiteReference

Enter the unique reference your organisation uses to identify the site.

If one doesn’t exist, you need to create one. It should not be used by your organisation to identify any other sites, but can be borrowed from another data set listing the site. You could use the strategic site identifier from your local plan, for example:

EH/141

#### SiteNameAddress

Enter the site name and address in a single line of text, for example:

Parcel of land behind, 221B Baker Street, Marylebone, London, NW1 6XE

#### GeoY

Enter the latitude of a point close to the centre of the site. The value should be 6 or fewer decimal places, using the WGS84 or ETRS89 coordinate systems specified by the [open standards for government guidance](https://www.gov.uk/government/publications/open-standards-for-government/exchange-of-location-point).

#### GeoX

Enter the longitude of a point close to the centre of the site. The value should be 6 or fewer decimal places, using the WGS84 or ETRS89 coordinate system specified by the [open standards for government guidance](https://www.gov.uk/government/publications/open-standards-for-government/exchange-of-location-point).

Be sure you do not mix up the latitude (Geo Y) and longitude (Geo X) values. Any location in the UK will have a latitude (Geo Y) from about 49 to 57 and a longitude (Geo X) from about -7 to 2.

If any of the following fields are unknown or unclear to your organisation, you can leave them blank:

#### SiteplanURL

Enter the URL of a web page hosting the site plan, beginning with either “http://” or “https://”.

#### Hectares

Enter the land area of the site in hectares, up to 2 decimal places. Use digits (2) rather than words (two).

#### OwnershipStatus

Indicate the site’s ownership by entering one of the following values:

- owned by a public authority
- not owned by a public authority
- mixed ownership

If the ownership is unknown or partly unknown, enter ‘unknown ownership’.

For more information see paragraph 5 of [Schedule 2 of the 2017 Regulations](http://www.legislation.gov.uk/uksi/2017/403/schedule/2/made).

#### PlanningStatus

Choose one of the following to indicate what stage of the planning process the site is at:

- permissioned
- not permissioned
- pending decision

When part of a site is permissioned, it should be recorded as “permissioned” and you should explain in the ‘Notes’ field why it’s only partly permissioned.

For more information see paragraph 5 of [Schedule 2 of the 2017 Regulations](http://www.legislation.gov.uk/uksi/2017/403/schedule/2/made).

#### PermissionType

Choose one of the following to indicate what permission type the site has:

- full planning permission
- outline planning permission
- reserved matters approval
- permission in principle
- technical details consent
- planning permission granted under an order
- other

‘Planning permission granted under an order’ means planning permission granted under a local development order, a mayoral development order or a neighbourhood development order.

Where more than one permission exists for the site, identify the latest permission granted. List any other permissions, including the date that each permission was granted or deemed to have been granted, in the ’Notes’ column.

#### PermissionDate

Enter the date the most recent permission was granted on the site, in the format YYYY-MM-DD. If no permission has been granted leave this blank.

#### PlanningHistory

Enter links to any web pages that give information on the site’s planning history (include the “http://” or “https://” prefix). Fields in this column can contain more than one link, as long as you separate multiple links with the pipe character (‘|’). You can leave this field blank.

#### Deliverable

Enter ‘yes’ if there is a reasonable prospect that residential development will take place on the land within 5 years of the date you enter this site in the register. Otherwise leave this field blank.

#### NetDwellingsRangeFrom

Enter the minimum number of dwellings that the local planning authority estimates the site should support, as defined in [regulation 2 of the 2017 Regulations](http://www.legislation.gov.uk/uksi/2017/403/regulation/2/made).

#### NetDwellingsRangeTo

Enter the maximum number of dwellings that the local planning authority estimates the site should support, as defined in [regulation 2 of the 2017 Regulations](http://www.legislation.gov.uk/uksi/2017/403/regulation/2/made).

#### HazardousSubstances

Enter ‘yes’ if the local planning authority is required by [regulation 26(3) of the Planning (Hazardous Substances) Regulations 2015](https://www.legislation.gov.uk/uksi/2015/627/regulation/26/made) to conduct an environmental impact assessment on the proposed development. Otherwise leave this blank.

#### Notes

Enter any general information about a site that developers might find useful, including a description of any housing development proposed for the site.

You may include links to any web pages that give:

- information on planning decisions related to any environmental impact assessments
- the results of any related consultations
- an explanation of how they were taken into account when making the decisions

You may also describe any non-housing development proposed for the site. Indicate how the buildings or land will be used, and the scale of any such development.

Content in this field does not need to be on a single line, but should be no longer than 4,000 characters. You can leave this field blank.

#### FirstAddedDate

Enter the date that the site was first added to this register, in the format YYYY-MM-DD.

#### LastUpdatedDate

Enter the date this entry in the register was updated, in the format YYYY-MM-DD.

#### EndDate

If the site no longer needs to be listed (for example, if the site has been built on), it should remain on the register for historical reasons and not be deleted. Enter the date the site was developed or determined to no longer be brownfield land, in the format YYYY-MM-DD. This field should only be filled in once the site is no longer classified as brownfield land.

### Check and provide your data

We’ve developed a tool which you can use to [check and provide your brownfield site data](https://submit.planning.data.gov.uk/).

## Step 2: Update your brownfield land web page

To complete step 2 you must be able to edit (or create) your local planning authority’s brownfield land web page. If you aren’t able or authorised to do this, speak to someone who is (this might be the person who updates your developer contribution or planning application web pages).

Upload the brownfield land CSV file to your local planning authority’s website. Make sure the URL for the CSV file is a [persistent URL](https://en.wikipedia.org/wiki/Persistent_uniform_resource_locator) (a web address that will not change over time). For example, Norfolk’s local planning authority might use the following persistent URL (this is an example, not live data):

https://www.norfolk.gov.uk/brownfield-land.csv

You should then update your brownfield land web page to make the CSV file publicly available.

The page must list the persistent URL as defined above. The URLs must be written out in full. The URL should not change. However, if it ever does change, you must tell us.

### Licensing

You must state on your web page that the data is provided under the [Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

Before you publish your web page, please check if you need to [inform the Ordnance Survey](https://www.ordnancesurvey.co.uk/business-government/licensing-agreements/public-sector-derived-data) that you are publishing this data.

## Step 3: Update the national brownfield land register

The Ministry of Housing, Communities and Local Government will maintain a national brownfield land register using the data you publish.

The first time you create and publish your CSV file, you must tell us where this is published (the persistent URL created in step 2). You must also tell us if this URL ever changes.

You can use the [check and provide service](https://provide.planning.data.gov.uk/) to submit your URL, or email the persistent URL for the CSV file to [DigitalLand@communities.gov.uk](mailto:DigitalLand@communities.gov.uk) and we will add it to the national register.

We also recommend that you add the URL to [data.gov.uk](http://data.gov.uk).

If you have any questions or feedback, email [DigitalLand@communities.gov.uk](mailto:DigitalLand@communities.gov.uk)
