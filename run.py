from API.api_wrapper import ApiWrapper
from COMMAND.line_command import line_args
from DB.db_implementation import Activity_DB



if line_args.action == 'new':
    activity_params = {
        'type': line_args.type,
        'participants': line_args.participants,
        'price_min': line_args.price_min,
        'price_max': line_args.price_max,
        'accessibility_min': line_args.accessibility_min,
        'accessibility_max': line_args.accessibility_max
    }

    with Activity_DB() as my_db:
        wrapper = ApiWrapper()
        activity = wrapper.get_response(**activity_params)
        my_db.create_field(activity)

        print(activity)
else:
    with Activity_DB() as my_db:
        latest_entries = my_db.get_latest_entries(quantity=5)

        print(latest_entries)

