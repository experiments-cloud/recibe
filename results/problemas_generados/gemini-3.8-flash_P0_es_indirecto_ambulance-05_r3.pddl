(define (problem ambulance_problem)
  (:domain ambulance)
  (:objects
    l1 l2 l3 l4 l5 - location
    amb1 - ambulance
    p1 p2 p3 p4 - patient
  )
  (:init
    (connected l1 l2)
    (connected l2 l1)
    (connected l2 l3)
    (connected l3 l2)
    (connected l4 l2)
    (connected l2 l4)
    (connected l2 l5)
    (connected l5 l2)
    (hospital l2)
    (ambulance-at amb1 l4)
    (empty amb1)
    (patient-at p1 l3)
    (patient-at p2 l1)
    (patient-at p3 l4)
    (patient-at p4 l3)
  )
  (:goal (and
    (patient-at p1 l2)
    (patient-at p2 l2)
    (patient-at p3 l2)
    (patient-at p4 l2)
  ))
)
