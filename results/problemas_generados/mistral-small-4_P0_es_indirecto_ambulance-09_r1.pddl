(define (problem ambulance-problem)
  (:domain ambulance)
  (:objects
    l1 l2 l3 l4 l5 l6 - location
    amb1 amb2 - ambulance
    p1 p2 p3 p4 - patient
  )
  (:init
    ; Conexiones entre ubicaciones (doble sentido)
    (connected l1 l6)
    (connected l6 l1)
    (connected l6 l3)
    (connected l3 l6)
    (connected l3 l2)
    (connected l2 l3)
    (connected l2 l4)
    (connected l4 l2)
    (connected l4 l6)
    (connected l6 l4)
    (connected l6 l5)
    (connected l5 l6)
    (connected l5 l2)
    (connected l2 l5)
    ; Hospital en l4
    (hospital l4)
    ; Ambulancias en sus ubicaciones iniciales
    (ambulance-at amb1 l5)
    (ambulance-at amb2 l3)
    ; Pacientes en sus ubicaciones iniciales
    (patient-at p1 l3)
    (patient-at p2 l3)
    (patient-at p3 l5)
    (patient-at p4 l5)
    ; Ambulancias vacías inicialmente
    (empty amb1)
    (empty amb2)
  )
  (:goal (and
    ; Todos los pacientes deben estar en el hospital (l4)
    (patient-at p1 l4)
    (patient-at p2 l4)
    (patient-at p3 l4)
    (patient-at p4 l4)
  ))
)
