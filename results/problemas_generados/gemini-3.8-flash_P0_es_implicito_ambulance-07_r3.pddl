(define (problem transport-patients)
  (:domain ambulance)
  (:objects
    l1 l2 l3 l4 l5 l6 - location
    amb1 amb2 - ambulance
    p1 p2 - patient
  )
  (:init
    (connected l1 l4)
    (connected l4 l1)
    (connected l2 l3)
    (connected l3 l2)
    (connected l2 l4)
    (connected l4 l2)
    (connected l2 l5)
    (connected l5 l2)
    (connected l5 l6)
    (connected l6 l5)
    (hospital l4)
    (ambulance-at amb1 l6)
    (empty amb1)
    (ambulance-at amb2 l2)
    (empty amb2)
    (patient-at p1 l2)
    (patient-at p2 l3)
  )
  (:goal (and
    (patient-at p1 l4)
    (patient-at p2 l4)
  ))
)
