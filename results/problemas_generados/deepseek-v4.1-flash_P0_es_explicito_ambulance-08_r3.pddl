(define (problem ambulance-problem)
  (:domain ambulance)
  (:objects
    l1 - location
    l2 - location
    l3 - location
    l4 - location
    l5 - location
    l6 - location
    l7 - location
    amb1 - ambulance
    amb2 - ambulance
    p1 - patient
    p2 - patient
    p3 - patient
  )
  (:init
    (connected l1 l5)
    (connected l1 l6)
    (connected l2 l5)
    (connected l2 l7)
    (connected l3 l6)
    (connected l4 l5)
    (connected l5 l1)
    (connected l5 l2)
    (connected l5 l4)
    (connected l6 l1)
    (connected l6 l3)
    (connected l7 l2)
    (hospital l4)
    (ambulance-at amb1 l4)
    (ambulance-at amb2 l6)
    (empty amb1)
    (empty amb2)
    (patient-at p1 l2)
    (patient-at p2 l6)
    (patient-at p3 l1)
  )
  (:goal
    (and
      (patient-at p1 l4)
      (patient-at p2 l4)
      (patient-at p3 l4)
    )
  )
)
