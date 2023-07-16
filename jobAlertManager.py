import time
import schedule
import requests
import datetime
import pytz
import smtplib


def run():
    if is_summer_2024_job_posted():
        send_email()
        return False
    else:
        output_file = open("output.log", "a")
        output_file.write("No Job found at : " + str(datetime.datetime.now()) + "\n")
        output_file.close()
        return True


def is_summer_2024_job_posted():
    next_page_present = True
    i = 0

    while next_page_present:
        URL = 'https://www.amazon.jobs/en/search.json?normalized_country_code%5B%5D=USA&radius=24km&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&offset=' + str(
            i * 10) + '&result_limit=10&sort=recent&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&business_category%5B%5D=student-programs&'
        res = requests.get(URL)
        for job in res.json()['jobs']:
            title = str(job['title']).upper()
            if ("summer".upper() in title) and ("2024" in title):
                return True
        if len(res.json()['jobs']) < 10:
            next_page_present = False
        i = i + 1

    return False


def send_email(is_daily_remainder):
    output_file = open("output.log", "a")

    output_file.write("Sending email..!" + str(datetime.datetime.now()) + "\n")
    fromMy = 'rahulmora007@yahoo.com'  # fun-fact: "from" is a keyword in python, you can't use it as variable.. did anyone check if this code even works?
    to = 'rahulmora007@yahoo.com'
    date = datetime.datetime.today().strftime("%d/%m/%Y")
    if not is_daily_remainder:
        message_text = '!!!! HURRYYY !!!!\n Summer 2024 internship application is posted! Apply ASAP.'
        output_file.write("Job Posted Notification!!!" + "\n")
        subj = '!!!HURRY!!!! Amazon Job Posting released'
    else:
        subj = 'Acknowledgement notification'
        output_file.write("Acknowledgement notification!" + "\n")
        message_text = 'Job Notification program is running!'

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (fromMy, to, subj, date, message_text)

    username = str('rahulmora007@yahoo.com')
    password = str('tvvrasnpurzbfpdh')

    server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", port=465)
    server.login(user=username, password=password)
    server.sendmail(fromMy, to, msg)
    server.quit()
    output_file.write('ok the email has sent ' + str(datetime.datetime.now()) + "\n")

    output_file.close()


if __name__ == "__main__":
    # Get the current time in Eastern Standard Time (EST)
    est = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(est)
    schedule.every().day.at("12:00").do(send_email, True)
    schedule.every().day.at("20:00").do(send_email, True)
    schedule.every().day.at("04:00").do(send_email, True)
    schedule.every(10).minutes.do(run)

    global output_file

    output_file = open("output.log", "w")
    output_file.close()

    while True:
        schedule.run_pending()
        time.sleep(1)
