(define (problem logistics-problem)
 (:domain logistics)
 (:objects
   tru1 tru2 - truck
   apn1 - airplane
   obj11 obj12 obj13 obj21 obj22 obj23 - package
   pos1 pos2 apt1 apt2 - place
   cit1 cit2 - city
 )
 (:init
   (in-city pos1 cit1)
   (in-city pos2 cit2)
   (in-city apt1 cit1)
   (in-city apt2 cit2)
   (at tru1 pos1)
   (at tru2 pos2)
   (at apn1 apt2)
   (at obj11 pos1)
   (at obj12 pos1)
   (at obj13 pos1)
   (at obj21 pos2)
   (at obj22 pos2)
   (at obj23 pos2)
 )
 (:goal (and
   (at obj13 apt1)
   (at obj12 apt2)
   (at obj21 apt2)
   (at obj11 pos2)
 ))
)
