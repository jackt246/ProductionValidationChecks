


class qScoreChecks():
    '''This class is designed to run checks on the FSC curve of every entry staged for release. Each check should be added as a function and then called in RunChecksPerCheck.py'''
    def __init__(self, inputFile):
        self.inputFile = inputFile

        try:
            self.qScoreDataAll = self.inputFile['qscore']['0']['data']['qscore']
        except KeyError as e:
            raise Exception(f"Error: Required data not found in the JSON file. {e}")


    def proportionUnderZero(self):
        data = self.qScoreDataAll
        count_less_than_zero = len([num for num in data if num < 0])
        proportion = count_less_than_zero / len(data) if len(data) > 0 else 0
        return proportion

