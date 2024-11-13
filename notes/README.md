I'm reaching the end of my time working on this project, and it'll be apparent that there is a lot more that can be done
to improve the pipeline in code, but I will document my thoughts on what those next steps are to achieve this.

## Status

To start, I've primarily focused on maintainability, testability, durability, and observability. 
I've imposed a few rules that I think help enforce this.

- No task can depend on another task, all execution must happen at the top level (pipeline). 
This should minimize the dependency nightmare that can exist when a situation of nested tasks exist.

- I've added a rough signature analysis tool to verify that task annotations can be verified at runtime.
This should ensure that as data is passed between tasks, we assert that the proper types are being handed off at 
each step. In conjunction with static type checking, we can at least know that we're transforming data somewhat as
we expect. This is especially important if we have tasks that are transforming data. Maybe less so if they are
orchestrating some behavior, which is why it is optional (skipped if inspect._empty).

- I've removed all of the non-configuration execution of tasks to a separate function. This allows the methods
to be tested independently of the orchestration suite that normally runs the code. It means code can potentially be
packaged and redistributed if it needs to be used in multiple places, orchestration, app, etc.

- I've added a remote source for the backing data source of the application. In general, if our source of truth 
is stored in an external location, it can be updated independently of the app. There are pros and cons to this approach,
in this case it adds some accessibility and a much more manageable update should the dictionary need to change. We can package a backup with the application so it's always able to do it's job, and an override should an external source prove to be too difficult to maintain.

- I've also added some retry logic within the task for the rather general "Exception". In general I wouldn't have something so widely scoped, but I think it's a good reference for things like network outages, backoffs, etc.

## Next steps

A quick execution of this will show that my changes are slow and there's not really much in terms of scalability. I did not get to the efficiency gains that I wanted to implement, but I can describe what my thoughts were.

For the most part, the easiest win is to add some sort of threading to the word split. Any sort of multi-processing for the individual words would have resulted in some massive gains. But given some of the rules I've implemented it would have slightly broken some of the paradigms.

Ideally, this would be accomplished by adding custom outputs that handle the threading process with limits on maximum number of execution units. I think this is better shown within the orchestration engine rather than having the developer attempt to implement it. Generally, threading gets tricky.

In a more ideal world - most of this could be thrown over to k8s where the scheduler and config could manage execution. The infrastructure is quite an important part of an successful orchestration/pipelining process.

I did implement a light caching on the permutations side, it might help a bit, but not enough when there are more than 1 word to analyze.