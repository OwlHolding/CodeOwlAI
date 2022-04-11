import os
import sys

def getpaths(templatespath='', solutionspath=''):
    """Return (path_to_templates, path_to_solutions) else FileNotFoundError"""
    
    path = os.path.abspath(__file__)
    abovedir = os.path.split(path)[0]
    doubleabovedir = os.path.split(abovedir)[0]
    templatespath = templatespath.replace('$local', abovedir)
    solutionspath = solutionspath.replace('$local', abovedir)

    if templatespath:
        pass
    elif os.path.isdir(abovedir + "\\templates"):
        templatespath = abovedir + "\\templates"
    elif os.path.isdir(doubleabovedir + "\\templates"):
        templatespath = doubleabovedir + "\\templates"
    else:
        raise FileNotFoundError("Templates directory not found")

    if solutionspath:
        pass
    elif os.path.isdir(abovedir + "\\solutions"):
        solutionspath = abovedir + "\\solutions"
    elif os.path.isdir(doubleabovedir + "\\solutions"):
        solutionspath = doubleabovedir + "\\solutions"
    else:
        raise FileNotFoundError("Solutions directory not found")

    return templatespath, solutionspath

class AuroraPredictor():
    "Aurora Assistant Predictor"

    def __init__(self, templatespath='', solutionspath='') -> None:
        self.templatespath, self.solutionspath = getpaths(
            templatespath, solutionspath)
    
    def predict(self, traceback):
        templates = os.listdir(self.templatespath)
        for i in templates:
            with open(f'{self.templatespath}/{i}') as f:
                features = map(lambda x: x.replace('\n', ''), f.readlines())
                features = map(lambda x: x.replace('  ', ' '), features)
            flag = True
            for feature in features:
                if traceback.find(feature) == -1:
                    flag = False
            if flag:
                with open(f'{self.solutionspath}/{i}') as f:
                    return f.read()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            traceback = f.read()
        model = AuroraPredictor()
        print(model.predict(traceback))
    else:
        print("Please pass the traceback path as a command line argument")
