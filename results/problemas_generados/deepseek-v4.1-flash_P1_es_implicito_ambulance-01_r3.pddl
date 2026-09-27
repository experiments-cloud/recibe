(define (problem ambulance-problema)
  (:domain ambulance)
  (:objects
    amb1 - ambulance
    l1 l2 l3 l4 - location
    p1 p2 p3 p4 - patient
  )
  (:init
    (ambulance-at amb1 l4)
    (connected l1 l4)
    (connected l4 l1)
    (connected l2 l3)
    (connected l3 l2)
    (connected l2 l4)
    (connected l4 l2)
    (connected l3 l4)
    (connected l4 l3)
    (empty amb1)
    (hospital l2)
    (patient-at p2 l1)
    (patient-at p3 l3)
    (patient-at p4 l3)
    (patient-at p1 l4)
  )
  (:goal (and
    (patient-at p1 l2)
    (patient-at p2 l2)
    (patient-at p3 l2)
    (patient-at p4 l2)
  ))
)
