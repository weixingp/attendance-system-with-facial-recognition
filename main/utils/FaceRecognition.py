import face_recognition

from main.models import LabGroupStudentPair


class FaceRecognitionManager:

    def __init__(self, lab_group):
        """
        Init the manager with student's photos from specific lab group
        :param lab_group: LabGroup object
        """
        self.lab_group = lab_group
        self.records = []  # List of Student object - Photo encoding tuple pair
        students = []
        lab_students = LabGroupStudentPair.objects.filter(lab_group=self.lab_group)
        for lab_student in lab_students:
            students.append(lab_student.student)

        # Load face encodings
        for student in students:
            image = face_recognition.load_image_file(student.photo)
            encoding = face_recognition.face_encodings(image)[0]
            self.records.append((student, encoding))

    def recognise_student(self, photo):
        unknown_image = face_recognition.load_image_file(photo)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if len(unknown_encodings) == 0:
            # No face detected in the photo
            return False
        else:
            unknown_encoding = unknown_encodings[0]

        for record in self.records:
            student = record[0]
            encoding = record[1]
            match = face_recognition.compare_faces(encoding, unknown_encoding, tolerance=0.45)
            if match:
                # Return the student obj if match found
                return student

        return False

    @staticmethod
    def check_photo(photo):
        # Check if only 1 face can be detected
        image = face_recognition.load_image_file(photo)
        encoding = face_recognition.face_encodings(image)

        if len(encoding) == 0 or len(encoding) > 1:
            return False
        else:
            return True


# yizhen_image = face_recognition.load_image_file("photos/k1.jpg")
# print(len(face_recognition.face_encodings(yizhen_image)))
# yizhen_encoding = face_recognition.face_encodings(yizhen_image)[0]
#
# # claris_image = face_recognition.load_image_file("photos/tommy4.jpg")
# # claris_encoding = face_recognition.face_encodings(claris_image)[0]
#
#
# unknown_image = face_recognition.load_image_file("photos/claris.jpg")
# unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
#
# print("recognising...")
# face_distances = face_recognition.face_distance([yizhen_encoding], unknown_encoding)
#
# print(face_distances)
#
# for i, face_distance in enumerate(face_distances):
#     print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
#     print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
#     print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
#     print()

# matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
# print(matches)