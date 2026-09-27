(define (problem ambulance-problem)
  (:domain ambulance)
  (:objects
    l1 - location
    l2 - location
    l3 - location
    l4 - location
    l5 - location
    amb1 - ambulance
    p1 - patient
    p2 - patient
    p3 - patient
    p4 - patient
  )
  (:init
    (connected l2 l4)
    (connected l4 l2)
    (connected l4 l1)
    (connected l1 l4)
    (connected l1 l3)
    (connected l3 l1)
    (connected l4 l5)
    (connected l5 l4)
    (hospital l3)
    (ambulance-at amb1 l1)
    (empty amb1)
    (patient-at p2 l2)
    (patient-at p1 l5)
    (patient-at p3 l5)
    (patient-at p4 l5)
  )
  (:goal
    (and
      (patient-at p1 l3)
      (patient-at p2 l3)
      (patient-at p3 l3)
      (patient-at p4 l3)
    )
  )
)
