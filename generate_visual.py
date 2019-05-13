import calendar
from datetime import datetime, timedelta
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pytz
import traceback


class GenerateVisual:

    def __init__(self, username='s3652122', api_key='waPS3YMdkvNPuO7XXgAA'):
        # fill in plotly username and api key
        py.sign_in(username=username, api_key=api_key)

    def graph_weekly_data(self, query):
        bookCategory = self.weekly_book_category(query)
        dateCategory = self.weekly_date_category(query)
        if bookCategory is True and dateCategory is True:
            return True
        return False

    def graph_daily_data(self, query):
        return False

    def weekly_book_category(self, query):
        books = []
        count = []
        try:
            for q in query:
                book = q["ISBN"]
                if book not in books:
                    books.append(q["ISBN"])
                    count.append(1) 
                else:    
                    for i in range(len(books)):
                        if book == books[i]:
                            count[i] += 1
                            break
            
            trace = go.Bar(
                x=books,
                y=count
            )

            layout = go.Layout(
                title='Number of times book borrowed'
            )
            data = [trace]
            fig = go.Figure(data=data, layout=layout)
            py.plot(data, filename="weekly_by_book")
            return True
        except Exception:
            print("Error generate weekly_book_category graph: ")
            traceback.print_exc()
            return False    

    def weekly_date_category(self, query):
        dates = []
        count = []
        try:
            for q in query:
                date = q["borrowDate"].strftime("%Y-%m-%d")
                if date not in dates:
                    dates.append(date)
                    count.append(1)
                else:
                    for i in range(len(dates)):
                        if date == dates[i]:
                            count[i] += 1
                            break
            trace = go.Scatter(
                x=dates,
                y=count
            )

            layout = go.Layout(
                title=go.layout.Title(
                    text='Number of books borrowed by date'
                ),
                xaxis=go.layout.XAxis(
                    title=go.layout.xaxis.Title(
                        text='Date',
                        font=dict(
                            family='Courier New, monospace',
                            size=15
                        )
                    ) 
                ),
                yaxis=go.layout.YAxis(
                    title=go.layout.yaxis.Title(
                        text='Num of books',
                        font=dict(
                            family='Courier New, monospace',
                            size=15
                        )
                    ) 
                )
            )

            data = [trace]
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='weekly by date')        
            return True
        except Exception:
            print("Error generate weekly_day_category graph: ")
            traceback.print_exc()
            return False            