(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
  )
  (:init
    (ontable d)
    (on a f)
    (on b a)
    (on c d)
    (on e g)
    (on f c)
    (on g b)
    (clear e)
    (handempty)
  )
  (:goal
    (and
      (on a g)
      (on b c)
      (on c f)
      (on d b)
      (on f e)
      (on g d)
    )
  )
)
