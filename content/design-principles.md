---
name: Design principles
---
Follow these principles when you design planning data.

## 1. Model the world, not existing data

Design data that represents real things and how they relate to each other.
Do not copy existing data sources, formats, and schemas. 

We can collect data in many different ways, and make it available to users in many different forms,
but the core concepts of data on the platform needs to reflect reality.

Find out how to:

* [start with user needs](https://www.gov.uk/guidance/government-design-principles#start-with-user-needs)  
* [model entities and relationships](https://en.wikipedia.org/wiki/Ontology_\(information_science\))

## 2. Use precise terms

Names in your data model must be simple, clear, and only have one meaning.
Do not use product names, abbreviations, or acronyms.
They are often unclear and can go out of date quickly.

Each term should have an official definition from legislation, policy, or other trusted source. 
If you cannot find a good definition, choose a short, plain English term and test it with users.

Find out more about:

* [how to be consistent, not uniform](https://www.gov.uk/guidance/government-design-principles#be-consistent-not-uniform)
* [domain driven design](https://en.wikipedia.org/wiki/Domain-driven_design)
* [citations](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)

## 3. Do not repeat information

Repeating information makes mistakes more likely and means values can stop matching. 
Repeated information also makes data harder to update and bigger to store.
For example, if you repeat the local authority’s name on every planning application, 
you will have to change every planning application if the local authority changes its name.

Learn about:

* [tidy data principles](https://www.gov.uk/government/statistics/personal-and-stakeholder-pensions-statistics/tidy-data-guide)  
* [the do not repeat yourself principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)  
* [database normalisation](https://en.wikipedia.org/wiki/Database_normalization)

## 4. Only include what is needed

Do not add everything that relates to a dataset.
Only include the core data that users need to act or make a decision, or that the law requires.

Design the data you know users need, not what people say they want or think might be useful.

Only ask people for information they are responsible for. 
Do not ask for data that you can easily work out, or that someone else manages more reliably.
Every field you add makes more work for the people providing the data, which often lowers its quality.

You should:

* [do less](https://www.gov.uk/guidance/government-design-principles#do-less)  
* [do the hard work to make it simple](https://www.gov.uk/guidance/government-design-principles#do-the-hard-work-to-make-it-simple)

## 5. Link to sources

Information in your data model can come from many places, but each fact should have one authoritative source.
Linking each fact to its source helps users to check and trust the data.

Find about:

* [persistent resolvable identifiers](https://www.gov.uk/government/publications/open-standards-for-government/persistent-resolvable-identifiers)
* [reuse and linkage](https://www.ons.gov.uk/aboutus/transparencyandgovernance/datastrategy/dataprinciples#reuse-and-linkage)  

## 6. Keep a history of changes

Things change over time and the data must show those changes.
Many planning tasks rely on this, such as checking the effect of a policy or challenging a past decision.

Deleting old information makes data less trustworthy and less useful.
Your model must keep every record and value, then show clearly when they change.
This includes when they start and stop applying.

The exception is information added by mistake.
Remove it quickly, especially if it contains sensitive or personal information.
If an official record itself contains a mistake, keep it as it is.
If we recorded something incorrectly, you can remove it.
This is especially important for unusual values that distort statistics.

Find out more:

* [digital continuity](https://www.nationalarchives.gov.uk/information-management/manage-information/policy-process/digital-continuity/what-is-digital-continuity/)
* [no link left behind](https://gds.blog.gov.uk/2012/10/11/no-link-left-behind/)
* [cool URIs don't change](https://www.w3.org/Provider/Style/URI)

## 7. Ask for and give feedback &mdash; early and often

Be open by default.
Wherever you can, share draft specifications, models and documentation publicly.
This lets planning authorities, software suppliers and data users give feedback early.

Respond to feedback quickly and act on it, because this builds trust in the platform.
When you give feedback to others, make it useful and easy to act on.

You should [make things open: it makes things better](https://www.gov.uk/guidance/government-design-principles#make-things-open-it-makes-things-better)

## 8. Expect change and avoid breaking changes

Data standards need to evolve as legislation changes, and new users and needs emerge. 

Users of the platform should enable forwards compatibility by ignoring any unexpected fields added in a later version of a specification, or added as an extension to support a local use-case.

Conversely, your specifications must maintain backward compatibility whenever possible. 
This means not removing existing fields, or changing the meaning of values users depend upon.

Where a breaking change is unavoidable, it should be clearly communicated in advance, for example by marking a field as being deprecated before later removing it.

* <a href="https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle">Open-Closed principle</a>.

## 9. Some data is better than no data

Start small with the simplest of needs, with the clearest needs for data, which can be quickly met using data collected from the smallest number of sources.
Then work to improve data quality, coverage, and cover more use-cases over time through feedback loops.

This iterative approach gives the most immediate value to users, allowing you to test and prove a specification before committing to it as a standard.

* [Iterate, then iterate again](https://www.gov.uk/guidance/government-design-principles#iterate-then-iterate-again)

## 10. Show the benefits

Planning data is a public good that increases in value the more people use it.
To sustain the platform and justify the effort required to publish and maintain data
We need to clearly show that value.

Standard web analytics do not show real-world use. Popularity is not the same as impact:

* a user might download a dataset once and serve it downstream to millions of people
* an automated script or AI agent might make hundreds of API calls without creating any public value

Measuring benefit requires getting closer to users to understand the decisions, services, and policies data simplifies or makes possible. 
So when designing a dataset, you need to work with users to develop quantitative metrics on how the data is being used, and case studies which document the savings and benefits which arise from using the data, not just vainly measure hits and downloads.

* [Value of Public Sector Data Estimate](https://www.gov.uk/government/publications/value-of-public-sector-data-estimate/value-of-public-sector-data-estimate)
* [Design with data](https://www.gov.uk/guidance/government-design-principles#design-with-data)
