from utilities import overlay_activities

def get_overlay(activitydetails):
	""" get_overlay function takes the activities details json object and returns the campaignName."""
	for item in activitydetails:
		for key, value in item.items():
			if key in overlay_activities.overlay_dict.values():
				return value['campaignName']