(define (problem blocks-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear a)
    (handempty)
    (on a d)
    (on b f)
    (on d b)
    (on e c)
    (on f e)
    (ontable c)
  )
  (:goal (and
    (on e f)
    (on f a)
    (on a b)
    (on b c)
    (on c d)
  ))
)
