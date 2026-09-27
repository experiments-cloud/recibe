(define (problem blocks-6)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
  )
  (:init
    (ontable c)
    (on a d)
    (on d b)
    (on b f)
    (on f e)
    (on e c)
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
      (clear e)
    )
  )
)
