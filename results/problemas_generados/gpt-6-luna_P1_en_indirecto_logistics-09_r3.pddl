(define (problem logistics-problem)
  (:domain logistics)
  (:objects
    apn1 - airplane
    apt1 apt2 apt3 - airport
    cit1 cit2 cit3 - city
    pos1 pos2 pos3 - location
    obj11 obj12 obj13 obj21 obj22 obj23 obj31 obj32 obj33 - package
    tru1 tru2 tru3 - truck
  )
  (:init
    (at apn1 apt1)
    (at tru1 pos1)
    (at tru2 pos2)
    (at tru3 pos3)
    (at obj11 pos1)
    (at obj12 pos1)
    (at obj13 pos1)
    (at obj21 pos2)
    (at obj22 pos2)
    (at obj23 pos2)
    (at obj31 pos3)
    (at obj32 pos3)
    (at obj33 pos3)
    (in-city pos1 cit1)
    (in-city apt1 cit1)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
    (in-city pos3 cit3)
    (in-city apt3 cit3)
  )
  (:goal (and
    (at obj32 apt1)
    (at obj13 apt2)
    (at obj23 apt2)
    (at obj31 apt3)
    (at obj12 pos1)
    (at obj21 pos2)
    (at obj11 pos3)
    (at obj22 pos3)
  ))
)
