(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on f e)
    (on e b)
    (ontable b)
    (on d a)
    (on a c)
    (ontable c)
    (clear f)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
