(define (problem blocks-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on f e)
    (on e b)
    (ontable b)
    (clear f)
    (on d a)
    (on a c)
    (ontable c)
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
