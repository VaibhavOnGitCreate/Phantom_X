from win10toast_click import ToastNotifier
import webbrowser
import threading


toaster = ToastNotifier()


def open_insights():

    try:

        print("Opening Phantom_X Insights...")

        webbrowser.open("http://127.0.0.1:5000")

    except Exception as e:

        print("Error:", e)

    return 0   # CRITICAL FIX


def send_phantom_notification(risk_score, risk_category):

    title = f"Phantom_X — {risk_category}"

    message = (
        f"Risk Score: {risk_score}/100\n"
        f"Click to see detailed insights"
    )

    toaster.show_toast(

        title,

        message,

        duration=6,

        threaded=True,

        callback_on_click=open_insights

    )


# test
if __name__ == "__main__":

    send_phantom_notification(
        90,
        "HIGH RISK"
    )