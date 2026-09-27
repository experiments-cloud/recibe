(define (problem ambulance-problem)
  (:domain ambulance)
  (:objects
    l1 l2 l3 l4 l5 l6 - location
    amb1 amb2 - ambulance
    p1 p2 p3 - patient
  )
  (:init
    (connected l2 l5)
    (connected l5 l2)
    (connected l5 l1)
    (connected l1 l5)
    (connected l1 l3)
    (connected l3 l1)
    (connected l3 l6)
    (connected l6 l3)
    (connected l6 l1)
    (connected l1 l6)
    (connected l1 l4)
    (connected l4 l1)
    (connected l5 l6)
    (connected l6 l5)

    (hospital l3)

    (ambulance-at amb1 l4)
    (empty amb1)
    (ambulance-at amb2 l1)
    (empty amb2)

    (patient-at p1 l1)
    (patient-at p2 l6)
    (patient-at p3 l5)
  )
  (:goal
    (and
      (patient-at p1 l3)
      (patient-at p2 l3)
      (patient-at p3 l3)
    )
  )
)
