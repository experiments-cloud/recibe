(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (on e c)
    (on f e)
    (on b f)
    (on d b)
    (on a d)
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
