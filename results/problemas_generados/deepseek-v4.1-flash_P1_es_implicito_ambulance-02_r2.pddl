(define (problem ambulance-problema)
  (:domain ambulance)
  (:objects
    amb1 - ambulance
    l1 l2 l3 l4 - location
    p1 p2 - patient
  )
  (:init
    (connected l1 l3)
    (connected l3 l1)
    (connected l1 l4)
    (connected l4 l1)
    (connected l2 l4)
    (connected l4 l2)
    (hospital l1)
    (ambulance-at amb1 l3)
    (empty amb1)
    (patient-at p2 l2)
    (patient-at p1 l3)
  )
  (:goal (and
    (patient-at p1 l1)
    (patient-at p2 l1)
  ))
)
