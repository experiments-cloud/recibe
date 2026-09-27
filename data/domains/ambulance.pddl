;; Ambulance domain created for this study (classical STRIPS with typing).
(define (domain ambulance)
  (:requirements :strips :typing)
  (:types location ambulance patient)

  (:predicates
    (connected ?from - location ?to - location)
    (hospital ?l - location)
    (ambulance-at ?a - ambulance ?l - location)
    (patient-at ?p - patient ?l - location)
    (in ?p - patient ?a - ambulance)
    (empty ?a - ambulance))

  (:action drive
    :parameters (?a - ambulance ?from - location ?to - location)
    :precondition (and (ambulance-at ?a ?from) (connected ?from ?to))
    :effect (and (not (ambulance-at ?a ?from)) (ambulance-at ?a ?to)))

  (:action load
    :parameters (?p - patient ?a - ambulance ?l - location)
    :precondition (and (ambulance-at ?a ?l) (patient-at ?p ?l) (empty ?a))
    :effect (and (not (patient-at ?p ?l)) (not (empty ?a)) (in ?p ?a)))

  (:action unload
    :parameters (?p - patient ?a - ambulance ?l - location)
    :precondition (and (ambulance-at ?a ?l) (in ?p ?a))
    :effect (and (not (in ?p ?a)) (empty ?a) (patient-at ?p ?l)))
)
