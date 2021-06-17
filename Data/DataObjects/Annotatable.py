class Annotatable():
    def __init__(self):
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations.append(annotation)

    def get_specific_annotation(self, annotation_label):
        for annotation in self.annotations:
            if annotation.label == annotation_label:
                return annotation

        return None

    def get_annotations(self):
        return self.annotations