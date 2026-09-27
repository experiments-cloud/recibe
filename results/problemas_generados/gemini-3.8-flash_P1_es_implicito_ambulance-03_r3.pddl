(define (problem ambulance-problem)
  (:domain ambulance)
  (:objects
    amb1 - ambulance
    l1 l2 l3 l4 l5 - location
    p1 p2 - patient
  )
  (:init
    (ambulance-at amb1 l2)
    (empty amb1)
    (hospital l2)
    (connected l1 l4)
    (connected l4 l1)
    (connected l1 l5)
    (connected l5 l1)
    (connected l2 l4)
    (connected l4 l2)
    (connected l3 l4)
    (connected l4 l3)
    (connected l4 l5)
    (connected l5 l4)
    (patient-at p1 l1)
    (patient-at p2 l4)
  )
  (:goal (and
    (patient-at p1 l2)
    (patient-at p2 l2)
  ))
)
