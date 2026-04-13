import config
import sys
from analytics import *
import logging

if __name__ == "__main__":
    logging.info('Program started')

    if len(sys.argv) != 4: 
        print("Wrong argument") 
        logging.error('Wrong number of arguments')
        sys.exit(1)

    filename = sys.argv[1]
    output_filename = sys.argv[2]
    ext = sys.argv[3]

    filename = sys.argv[1]
    logging.info(f'Processing file: {filename}')

    try:
        r = Research(filename)
        data = r.file_reader()

        c = Calculations(data)
        a = Analytics(data)

        head, tail = c.counts()
        h_per, t_per = c.fractions(head, tail)
        predictions = a.predict_random(config.NUM_STEPS)

        c_pred = Calculations(predictions)
        head_pred, tail_pred = c_pred.counts()

        format_prediction = f"{tail_pred} tail and {head_pred} heads."
        
        report = config.REPORT_TEMPLATE.format(
            observations=head+tail,
            tail_count=tail,
            head_count=head,
            tail_percentage=t_per,
            head_percentage=h_per,
            prediction=format_prediction
        )
        
        saved_file = a.save_file(report, "report", "txt")
        print(f"Report saved to {saved_file}")
        r.sendMessage_TG(True)
        logging.info('Program completed successfully')

    except Exception as e:
        logging.error(f'Program failed with error: {e}')
        r = Research("dummy.txt") 
        r.sendMessage_TG(False)
        print(e)
        sys.exit(1)