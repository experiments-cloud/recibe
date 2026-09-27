(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a d b f e c - block
  )
  (:init
    (on a d)
    (on d b)
    (on b f)
    (on f e)
    (on e c)
    (ontable c)
    (clear a)
    (handempty)
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
