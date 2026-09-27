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
    (on c d)
    (on f c)
    (on a f)
    (on b a)
    (on g b)
    (on e g)
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
