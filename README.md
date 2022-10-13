# Small Jobs App

## TODO list
include tests for what we've written today

1. In my opinion, we must create "scenarios" and "use cases" for the website before starting coding.
2. Then, we should create the requirements for the programming perspectives (and create the programming environment).
3. After that we can come up with a design and start coding.

## Ideas

- We can use [Firebase](https://firebase.google.com/) for user authentication, database (we can store data in JSON trees), and analytics. It can be easily integrated, I am using Firebase in my Android apps.
- We should consider using [Bootstrap](https://getbootstrap.com/) for design purposes. This way we can create a responsive website much easier.
- We can host our website in Firebase as well if we only use HTML, CSS, and Javascript. Other languages (Python, PHP) are not allowed. OR we must find a free website hoster.
    - There might be a possibility that we can host the website using the uni's resources. We should ask Bruce or Brian about this.
    - Being able to use a different framework (such as Django or Flask which use Python) could allow us to have an easier time than if we have to learn JavaScript

## Concerns

- If we use an "in-app currency" or points, then we have to implement some mechanics to top up your balance to be able to post tasks for points.
  - What if we find a company that can sponsor the app while enabling spending points to buy their product?
- I was thinking that only the task-doers would earn points which would have no other material value or use other than purchasing items at the "store" an organization makes for themselves (while for posting it can be unlimited or decided by a subscription tier fees payed to us).
- I personally do love the company sponsorship idea (for discounts or freebies in the app), if it is feasible, because that really goes hand-in-hand with the goal of empowering local communities and businesses.
- Incentives need to be added in game theory, in a specific range, value of points needs to be calibrated so that people don't exploit it
- SCRIP systems, fiat money, studies about collapse when people game the system
- Should we manage rewards ourselves based on research and surveying within an organization/community about wants and needs?
- Who can post jobs?
- Security of data
- Background checks
- Risk that no one near would be interested in buying into the idea, is it that compelling then?
- Liability of damage
- Terms and Conditions


## Brief (working) overview:
A website/web app that gets people within an organization or community to perform tasks in exchange for points. These points behave like a digital currency in an "incentive shop" managed by the organizers.

### Use cases:
   - In an office to make daily operations smoother (e.g. coffee runs/brewing, replacing water in cooler, etc.)
   - By a town council to get people volunteering in a local capacity
   - In a school to incentivize students (cleaning boards, participating in certain extracurricular activities, etc.)

## Principal components:
- Portal for task posters
- Portal for bidders
- Incentive shop
- Databases
   - User management/permissions
   - App data (tasks, bids, etc.)
   - \+
- Ranking algorithms
   - Sorting
      - Parameters: value, how long a task been posted, urgency, etc.
- Rating of volunteers (behind the scenes)

## Unanswered Questions
- Should tasks have expirations?
- What mechanism is there to make sure tasks have been performed?

## Potential features
- Certificates to accredit people for having done volunteering work
