# reversal_detector.py


class ReversalDetector:
    @staticmethod
    def detect_reversal(previous_beat_dict, current_beat_dict):
        if not previous_beat_dict:
            return {"blue_reversal": False, "red_reversal": False}

        reversal_info = {"blue_reversal": False, "red_reversal": False}

        for hand in ["blue_attributes", "red_attributes"]:
            prev_prop_rot_dir = previous_beat_dict.get(hand, {}).get("prop_rot_dir")
            curr_prop_rot_dir = current_beat_dict.get(hand, {}).get("prop_rot_dir")
            if prev_prop_rot_dir and curr_prop_rot_dir:
                if prev_prop_rot_dir != curr_prop_rot_dir:
                    reversal_info[f'{hand.split("_")[0]}_reversal'] = True

        return reversal_info
