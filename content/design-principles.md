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

Anyone that uses data from the platform should ignore any fields they do not recognise.
These fields may be added:

* in a later version of a specification   
* as an extension to support a local use-case

When you update a specification, make sure it still works for existing users whenever possible.
Do not remove fields or change the meaning of values that people rely on.

If you must make a change that will stop things working for users, tell them well in advance.
For example, mark a field as being ‘deprecated’ before you remove it in a future specification.

[Learn about the open-closed principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle).

## 9. Some data is better than no data

Start small. Meet the simplest and clearest needs first, using data from as few sources as possible.
Then use feedback to improve quality and coverage, so that you meet more needs over time.

This gives users value sooner and lets you test a specification before you make it a standard.

[Iterate, then iterate again](https://www.gov.uk/guidance/government-design-principles#iterate-then-iterate-again).

## 10. Show the benefits

The more people that use data, the more valuable it becomes.
We need to show this value to justify the work of publishing the data and maintaining the platform.

Standard website analytics do not show real-world use, because popularity is not the same as impact.
For example:

* someone might download a dataset once and use it in a service that millions of people use  
* an automated script or AI tool might make hundreds of API requests without creating any public benefit

To measure benefit, work closely with users to understand which decisions, services and policies the data supports.
When you design a dataset, agree measures with users and write case studies that show real results, not just website traffic.

Find out more:

* [value of public sector data estimate](https://www.gov.uk/government/publications/value-of-public-sector-data-estimate/value-of-public-sector-data-estimate)  
* [design with data](https://www.gov.uk/guidance/government-design-principles#design-with-data)

