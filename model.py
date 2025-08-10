import cv2
import mediapipe as mp
import numpy as np
import open3d as o3d

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

vis = o3d.visualization.Visualizer()
vis.create_window(window_name="3D Face Model", width=800, height=600)
point_cloud = o3d.geometry.PointCloud()
line_set = o3d.geometry.LineSet()
first_frame = True

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands, \
     mp_face_mesh.FaceMesh(
         max_num_faces=1,
         refine_landmarks=True,
         min_detection_confidence=0.5,
         min_tracking_confidence=0.5
     ) as face_mesh:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False

        pose_results = pose.process(frame_rgb)
        hands_results = hands.process(frame_rgb)
        face_results = face_mesh.process(frame_rgb)

        frame_rgb.flags.writeable = True
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(0,128,0), thickness=2))

        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(128,0,0), thickness=2))

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,191,255), thickness=1))

                landmarks = face_landmarks.landmark
                points_3d = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])
                
                points_3d[:, 1] = -points_3d[:, 1]
                points_3d[:, 2] = -points_3d[:, 2]

                connections = list(mp_face_mesh.FACEMESH_TESSELATION)
                lines = np.array(connections)

                point_cloud.points = o3d.utility.Vector3dVector(points_3d)
                line_set.points = o3d.utility.Vector3dVector(points_3d)
                line_set.lines = o3d.utility.Vector2iVector(lines)
                line_set.paint_uniform_color([0.0, 0.7, 0.2])

                if first_frame:
                    vis.add_geometry(point_cloud)
                    vis.add_geometry(line_set)
                    first_frame = False
                else:
                    vis.update_geometry(point_cloud)
                    vis.update_geometry(line_set)

        vis.poll_events()
        vis.update_renderer()

        cv2.imshow("HDBVIA - 2D View", frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
vis.destroy_window()
