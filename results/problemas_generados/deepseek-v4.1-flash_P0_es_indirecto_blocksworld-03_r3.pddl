(define (problem blocks-tower)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear a)
    (handempty)
    (ontable c)
    (on a d)
    (on d b)
    (on b f)
    (on f e)
    (on e c)
  )
  (:goal
    (and
      (on e f)
      (on f a)
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
