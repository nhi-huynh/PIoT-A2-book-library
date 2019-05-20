import calendar
from datetime import datetime, timedelta
import plotly.plotly as ply
import plotly.graph_objs as go
import numpy as np
import pytz
import traceback


class GenerateVisual:

    def __init__(self):
        # fill in plotly username and api key
        ply.sign_in(username=username, api_key=api_key)

    def graph_weekly_data(self, query):
        bookCategory = self.weekly_book_category(query)
        dateCategory = self.weekly_date_category(query)
        if bookCategory is True and dateCategory is True:
            return True
        return False

    def graph_daily_data(self, query):
        hourCategory = self.daily_hour_category(query)
        if hourCategory is True:
            return True
        return False

    def weekly_book_category(self, query):
        books = []
        bookTitle = []
        count = []
        try:
            for q in query:
                book = q["ISBN"]
                if book not in books:
                    books.append(q["ISBN"])
                    getBookTable = q["book"]
                    bookTitle.append(getBookTable["Title"])
                    count.append(1) 
                else:    
                    for i in range(len(books)):
                        if book == books[i]:
                            count[i] += 1
                            break
            
            trace = go.Bar(
                x=bookTitle,
                y=count
            )

            layout = go.Layout(
                title='Number of times book borrowed'
            )
            data = [trace]
            fig = go.Figure(data=data, layout=layout)
            ply.plot(data, filename="weekly_by_book")
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
            ply.plot(fig, filename='weekly by date')        
            return True
        except Exception:
            print("Error generate weekly_day_category graph: ")
            traceback.print_exc()
            return False

    def daily_hour_category(self, query):
        borrow_times = []
        count = []
        date = None
        try:
            for q in query:
                if not date:
                    date = q["borrowDate"].strftime("%Y-%m-%d")
                borrowtime = q["borrowDate"].strftime("%H")
                if borrowtime not in borrow_times:
                    borrow_times.append(borrowtime)
                    count.append(1)
                else:
                    for i in range(len(borrow_times)):
                        if borrowtime == borrow_times[i]:
                            count[i] += 1
                            break
            trace = go.Scatter(
                x=borrow_times,
                y=count
            )

            layout = go.Layout(
                title=go.layout.Title(
                    text='Books borrowed on {}'.format(date)
                ),
                xaxis=go.layout.XAxis(
                    title=go.layout.xaxis.Title(
                        text='Hour',
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
            ply.plot(fig, filename='daily by hour')        
            return True
        except Exception:
            print("Error generate weekly_day_category graph: ")
            traceback.print_exc()
            return False                
