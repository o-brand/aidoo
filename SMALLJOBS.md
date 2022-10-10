# Small Jobs App Ideas

## TODO list

1. In my opinion, we must create "scenarios" and "use cases" for the website before starting coding.
2. Then, we should create the requirements for the programming perspectives (and create the programming environment).
3. After that we can come up with a design and start coding.

## Ideas

- We can use [Firebase](https://firebase.google.com/) for user authentication, database (we can store data in JSON trees), and analytics. It can be easily integrated, I am using Firebase in my Android apps.
- We should consider using [Bootstrap](https://getbootstrap.com/) for design purposes. This way we can create a responsive website much easier.
- We can host our website in Firebase as well if we only use HTML, CSS, and Javascript. Other languages (Python, PHP) are not allowed. OR we must find a free website hoster.

## Concerns

- If we use an "in-app currency" or points, then we have to implement some mechanics to top up your balance to be able to post tasks for points.
  - What if we find a company that can sponsor the app while enabling spending points to buy their product?


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
      + Parameters: value, how long a task been posted, urgency, etc.

## Unanswered Questions
- Should tasks have expirations?
- What mechanism is there to make sure tasks have been performed?

## Potential features
