from django.http import HttpResponse
from django.shortcuts import render
from . import JobListing,SendMail
from IPython.display import HTML
import pandas as pd

from django.http import FileResponse
new_result = ''
def download(request):
    # pre-processing, authorizations, etc.
    # ...
    return FileResponse(open("templates\Data\Job_data.csv", 'rb'), as_attachment=True)

def index(request):
    return render(request,"index.html")

def sendmail(request):
    sender = request.GET.get("sendermail")
    receiver = request.GET.get("receivermail")
    with open("templates/table.html") as file:
        html_content = file.read()
    SendMail.sendmail(html_content,sender,receiver)
    print("Mail Sent")

    return render(request,"result.html")

def fetch(request):
    name = request.GET.get("username")
    job = request.GET.get("job")
    count = int(request.GET.get("count"))
    count = int(count / 10)
    # print(count)
    data = JobListing.get_jobs(job,count)
    data.to_csv("templates\Data\Job_data.csv")
    print(data.columns)
    if "thumbnail" in data.columns:
        data = data.drop(["thumbnail"],axis=1)
    result = data.drop(["job_highlights","job_id","description","extensions"],axis=1)

    links_list = result['related_links']

    header = '''<!DOCTYPE html>
                <html>
                <head>
                <meta charset="ISO-8859-1">
                <title>Home Page</title>
                <title style="align-content: center;">Job Insights</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

                
                <style>
                    table{
                      margin: auto;
                      border: 1px solid black;
                    }
                    th{
                        padding: auto;
                        margin: auto;
                        background-color: rgb(255, 153, 0);
                        text-transform: capitalize;
                    }
                    .fade-in {
                        animation-name: fadeIn;
                        animation-duration: 10s;
                    }

                    @keyframes fadeIn {
                        from {
                            opacity: 0;
                        }
                        to {
                            opacity: 1;
                        }
                    }
                    .shake {
                    animation: shake 2s ease infinite;
                    }
                    @keyframes shake {
                        0%, 100% {transform: translateX(0);}
                        10%, 30%, 50%, 70%, 90% {transform: translateX(-10px);}
                        20%, 40%, 60%, 80% {transform: translateX(10px);}
                            }

                    .bounce-in-right {
                    animation: bounce-in-right 2s ease ;
                    }
                    @keyframes bounce-in-right {
                    0% {
                        opacity: 0;
                        transform: translateX(2000px);
                    }
                    60% {
                        opacity: 1;
                        transform: translateX(-30px);
                    }
                    80% { transform: translateX(10px); }
                    100% { transform: translateX(0); }
                    }

                    .bounce-out {
                    animation: bounce-out 2s ease infinite;
                    }
                    @keyframes bounce-out {
                    0% { transform: scale(1); }
                    25% { transform: scale(.95); }
                    50% {
                        opacity: 1;
                        transform: scale(1.1);
                    }
                    100% {
                        opacity: 0;
                        transform: scale(.3);
                    } 
                    }
                      /* Style buttons */
                  .btn {
                    background-color: DodgerBlue; /* Blue background */
                    border: none; /* Remove borders */
                    color: white; /* White text */
                    padding: 12px 16px; /* Some padding */
                    font-size: 16px; /* Set a font size */
                    cursor: pointer; /* Mouse pointer on hover */
                  }

                  input[type=email], select {
                    width: 80%;
                    padding: 10px 15px;
                    margin: 8px 0;
                    display: inline-block;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                  }

                </style>
            </head>
            <body>
                <header style="position: sticky; top: 0; z-index: 999;">
                    <nav class="navbar navbar-expand-md navbar-dark" style=" background-color: rgb(146, 47, 30); height: 120px;">
                        {% load static %}
                        <div><img src="{% static 'Logo/logo.png' %}", width="100" height="100" style="border:2px solid seashell;"></div>
                        <div class="shake">
                            <h1 class="navbar-brand"> Job Insights </h1>
                        </div>
                    </nav>
                 </header>    
<div style="padding: 15px; float:left;">
    <h5 style="font-family: 'Times New Roman', Times, serif;">Hello {{name}} !!!</h5>
    <h5 style=" font-family: 'Times New Roman', Times, serif;">Job profile: {{job}}</h5>
    <!-- <a href="demo.txt" download="demo.txt">Download File</a> -->
  </div>
  <div style="float: right; margin-top: 10px; margin-right: 10px;padding: 5px;">
    <a href="/download"><button class="btn"><i class="fa fa-download"></i> Download</button></a>

    <!-- Trigger the modal with a button -->
    <button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal"><i
        class="fa fa-envelope"></i> Send Mail</button>
  </div>
  
  <!-- Modal -->
  <div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Send Job Oppurtunities to friend</h4>

          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <div class="modal-body">
          <form action="/sendmail" ,method="GET">
            <label for="sendermail"> Sender Email: </label>
            <input type="email" name="sendermail" id="sendermail">
            <br>
            <label for="receivermail">Receiver Email: </label>
            <input type="email" name="receivermail" id="receivermail">
            <br>
            <button class="btn" type="submit">Send</button>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>

    </div>
  </div>

                '''

    newlist = []
    for links in links_list:
        grp = []
        for item in links:
            link = f'<a href="{item["link"]}">{item["text"]}</a>'
            grp.append(link)
        newlist.append(grp)
    result["related_links"] = newlist

    
    
    # Loop through each item in the list and replace the text with a link
    result = result.to_html(classes='table table-stripped')
    new_result = result.replace("&lt;","<")
    new_result = new_result.replace("&gt;",">")
    # print(type(result))



    # print("\nString Result\n",new_result)

    footer = '''</body>
</html>'''
  
    html_content = header+new_result+footer
    # write html to file
    html_file = open("./templates/result.html", "w")
    html_file.write(html_content)
    html_file.close()

    head = '''<!DOCTYPE html>
                <html>
                <head>
                <meta charset="ISO-8859-1">
                <title>Home Page</title>
                <title style="align-content: center;">Job Insights</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

                
                <style>
                    th{
                        padding: auto;
                        margin: auto;
                        background-color: rgb(255, 153, 0);
                        text-transform: capitalize;
                    }
                  </style>
                  </head>  
                  <body>'''
    tail = '''</body>
</html>'''
    html_file = open("./templates/table.html", "w")
    html_file.write(head+new_result+tail)
    html_file.close()

    params = {'name':name,'job':job, "data":new_result}
    return render(request,"result.html",params)