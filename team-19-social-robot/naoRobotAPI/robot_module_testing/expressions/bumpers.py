from naoqi import qi

import sys
import argparse

def onExpressionReport(expression_value):
    print ("Got ALExpressionWatcher signal with value: ", expression_value)
    # you can check the expression value, though report_mode=2 gauanteed it is true
    if expression_value:
        print ("You held the left bumber for at least 5 seconds, then let go!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qi-url", type=str, default="--qi-url=tcp://192.168.213.194:9559",
                        help="Robot ip address.")


    args = [parser.parse_args()]
    # Initialize qi framework by creating a local app and connecting to robot
    print("args", args)
    print("sys", sys.argv)
    ar = sys.argv
    ar.append("--qi-url=tcp://192.168.213.194:9559")

    app = qi.Application(ar)
    
    app.start()
    
    
    tts = app.session.service("ALTextToSpeech")
    

    # Make the robot say something
     # Make the robot say something asynchronously
    
    # --disable=re
    say_future = qi.async(tts.say, "Visit BBC News")  # type: ignore
    
    # Wait until the speaking is finished
    say_future.wait()
    
    # Print a message after speaking is complete
    print("NAO has finished speaking.")
    

    # Get a reference to the Expression Watcher service
    expression_svc = app.session.service("ALExpressionWatcher")

    # Setup the expression
    report_mode = 2  # see API doc for behavior of different report modes
    # The left bumper is not currently pressed, but 0.1 seconds ago, it was
    # pressed continuously for at least 5 seconds.
    expression_condition = "!'LeftBumperPressed' && ('LeftBumperPressed' ~ 5 @ 0.1)"

    # Add the expression, and get back an object representing it.
    # When this object goes out of memory scope, the expression is deleted.
    expression_obj = expression_svc.add(expression_condition, report_mode)
    # Connect expression object signal to a callback, which is called based on report_mode
    # To stop listening to this callback, you can call expression_obj.signal.disconnect(signal_id)
    signal_id = expression_obj.signal.connect(onExpressionReport)

    app.run() # Will block until the app connection is destroyed, or ctrl+c
