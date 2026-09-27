(define (problem blocks-6-0)
  (:domain blocks)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear d)
    (clear f)
    (handempty)
    (on a c)
    (on d a)
    (on e b)
    (on f e)
    (ontable b)
    (ontable c)
  )
  (:goal (and
    (on a e)
    (on b a)
    (on c b)
    (on e f)
    (on f d)
  ))
)
