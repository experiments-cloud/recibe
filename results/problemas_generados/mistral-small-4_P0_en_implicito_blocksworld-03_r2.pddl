(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on c e)
    (on e f)
    (on f b)
    (on b d)
    (on d a)
    (ontable c)
    (clear a)
    (handempty)
  )
  (:goal (and
    (on e f)
    (on f a)
    (on a b)
    (on b c)
    (on c d)
  ))
)
