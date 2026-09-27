(define (problem problema-logistica)
  (:domain logistics)
  (:objects
    pos1 pos2 pos3 - location
    apt1 apt2 apt3 - airport
    cit1 cit2 cit3 - city
    tru1 tru2 tru3 - truck
    apn1 - airplane
    obj11 obj12 obj13 obj21 obj22 obj23 obj31 obj32 obj33 - package
  )
  (:init
    ; Relaciones ciudad-lugar
    (in-city pos1 cit1)
    (in-city apt1 cit1)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
    (in-city pos3 cit3)
    (in-city apt3 cit3)

    ; Posiciones iniciales de camiones
    (at tru1 pos1)
    (at tru2 pos2)
    (at tru3 pos3)

    ; Posiciones iniciales de aviones
    (at apn1 apt2)

    ; Posiciones iniciales de paquetes
    (at obj11 pos1)
    (at obj12 pos1)
    (at obj13 pos1)
    (at obj21 pos2)
    (at obj22 pos2)
    (at obj23 pos2)
    (at obj31 pos3)
    (at obj32 pos3)
    (at obj33 pos3)
  )
  (:goal (and
    ; Meta 1: obj21 en aeropuerto de cit1
    (at obj21 apt1)

    ; Meta 2: obj13 y obj31 en aeropuerto de cit3
    (at obj13 apt3)
    (at obj31 apt3)

    ; Meta 3: obj11, obj12, obj22 y obj32 en ubicación urbana de cit1
    (at obj11 pos1)
    (at obj12 pos1)
    (at obj22 pos1)
    (at obj32 pos1)

    ; Meta 4: obj23 y obj33 en ubicación urbana de cit3
    (at obj23 pos3)
    (at obj33 pos3)
  ))
)
