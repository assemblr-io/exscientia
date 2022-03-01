# Exscientia Coding Challenge

This was a really interesting challenge for a few reasons, in particular I had to try and remember how to do a Lineweaver-Burk plot for inhibitor kinetics, and also I decided to do a web based python app using a library and IDE i haven't used before to try and challenge the creative element.

![Screen Shot 2022-02-25 at 9 51 01 am](https://user-images.githubusercontent.com/95592979/155639365-26db0312-fec7-4fb3-9aed-5eb8f4c00b0a.png)


## User Features

- A main scatter plot showing compound activity, coloured by the result type
- hovering over one of these points cross filters the two smaller charts to the left
- showing a sad excuse for a lineweaver-burk plot (top right) and a dose response curve below (right-bottom).
- the lineweaver-burk plot is not accurate as I didn't have all of the values (Km) OR know the inhibition type - but wanted to show how I would lay out the data if i did have it.  I would also have shown the R2 and fit to the data and x and y intercepts.

## Technical Features

- using dash/plotly and pandas for reading, creating dataframes and rendering components
- using PyCharm IDE and Python 3.8 interpreter to serve up the Flask app for viewing in a browser on http://127.0.0.1:8050/
- packages used are: dash, dash.dependencies, pandas and plotly.express

## Next Steps

- if i had more time, i'd be keen to try out a few other libraries as I found dash/plotly abstracted away styles/layout and made doing pretty a bit very unhelpful not fun magic!! :)
- integrate into a proper React app, and build a generic React/plotting app boilerplate
- allow for select and not just hover to cross-filter
- fix the Lineweaver so it extends and crosses the x-axis
- drop line on the dose-response curve showing the IC50 would be cool!
- attach more compound annotations showing compound info more simply


