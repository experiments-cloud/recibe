(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (ontable c)
    (on e c)
    (on f e)
    (on b f)
    (on d b)
    (on a d)
    (clear a)
    (handempty)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
      (on e f)
      (on f a)
    )
  )
)
